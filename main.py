import rss_fetch,sqlite3,os,datetime,time,argparse,mylog
from modules import cleanString
from myyaml import yamldef

def dumpp():
    start = time.time()

    try:
        os.mkdir("logs")
    except:
        pass

    db = sqlite3.connect("rss.db")
    cur = db.cursor()
    
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-k", "--Key", help = "Key from Userdata.yaml", default=None)
        
    # Read arguments from command line
    args = parser.parse_args()
    
    if args.Key:
        try: 
            site_name =  str(args.Key)
            site_url = str(yamldef()['sites'][str(args.Key)])
            try:
                cur.execute(f"drop trigger oldPost_delete_{site_name};")
            except:
                pass
            cur.execute(f"create table if not exists rss_data (id text primary key, title text not null, link text not null,summary text,author text, site text not null, time text not null, pub_day text not null, pub_date text not null, pub_month text not null, pub_year text not null, pub_time text not null);")
            cur.execute(f"create trigger if not exists oldPost_delete_{site_name} before insert on rss_data when (select count(id) from rss_data where site='{site_name}') > {int(yamldef()['min_articles_to_retain_per_website'])} begin delete from rss_data where id in (select id from rss_data where site='{site_name}' order by time asc limit 1); end;")
            posts_details, post_count = rss_fetch.get_posts_details(rss=site_url)
            for post in posts_details:
                try:
                    postTitle = cleanString(str(post["title"]))
                    insert_qry = f'insert into rss_data (id,title,link,summary,time,pub_day,pub_date,pub_month,pub_year,pub_time,author,site) values ("{post["id"]}", "{postTitle}","{post["link"]}","{post["summary"]}",datetime("now"),"{post["pub_day"]}" ,"{post["pub_date"]}" ,"{post["pub_month"]}","{post["pub_year"]}","{post["pub_time"]}","{post["author"]}","{site_name}");'
                    cur.execute(insert_qry)
                    #notification
                    db.commit()
                    mylog.logDef(loggLevel='info', logMSG=f">> ADDED: {site_name} [+] {postTitle}")
                    
                except Exception as error:
                    if str(error).split(" ")[0:3] == ['UNIQUE', 'constraint', 'failed:']:
                        pass
                    else:
                        mylog.logDef(loggLevel='error', logMSG=f">> ERROR: {site_name} [!] {postTitle} -> {error}")

            end = time.time()
            mylog.logDef(loggLevel='info', logMSG=f"Last ran on {datetime.datetime.now()} for site: {site_name}")
            mylog.logDef(loggLevel='info', logMSG=f"Completed in: {round((end-start)*10**3/1000, 5)} Seconds")

        except Exception as argsError:
            mylog.logDef(loggLevel='error', logMSG=f">> ERROR: {argsError}, maybe there is no site in the given list")
    else:
        for siteI in yamldef()['sites']:
            site_name = str(siteI)
            site_url = str(yamldef()['sites'][siteI])

            cur.execute(f"create table if not exists rss_data (id text primary key, title text not null, link text not null,summary text,author text, site text not null, time text not null, pub_day text not null, pub_date text not null, pub_month text not null, pub_year text not null, pub_time text not null);")
            cur.execute(f"create trigger if not exists oldPost_delete_{site_name} before insert on rss_data when (select count(id) from rss_data where site='{site_name}') > {int(yamldef()['min_articles_to_retain_per_website'])} begin delete from rss_data where id in (select id from rss_data where site='{site_name}' order by time asc limit 1); end;")
            posts_details, post_count = rss_fetch.get_posts_details(rss=site_url)
            for post in posts_details:  
                try:
                    postTitle = cleanString(str(post["title"]))
                    insert_qry = f'insert into rss_data (id,title,link,summary,time,pub_day,pub_date,pub_month,pub_year,pub_time,author,site) values ("{post["id"]}", "{postTitle}","{post["link"]}","{post["summary"]}",datetime("now"),"{post["pub_day"]}" ,"{post["pub_date"]}" ,"{post["pub_month"]}","{post["pub_year"]}","{post["pub_time"]}","{post["author"]}","{site_name}");'
                    cur.execute(insert_qry)
                    #notification
                    db.commit()
                    mylog.logDef(loggLevel='info', logMSG=f">> ADDED: {site_name} [+] {postTitle}")
                
                except Exception as error:
                    if str(error).split(" ")[0:3] == ['UNIQUE', 'constraint', 'failed:']:
                        pass
                    else:
                        mylog.logDef(loggLevel='error', logMSG=f">> ERROR: {site_name} [!] {postTitle} -> {error}")
        
        end = time.time()
        mylog.logDef(loggLevel='info', logMSG=f"Last ran on {datetime.datetime.now()}")
        mylog.logDef(loggLevel='info', logMSG=f"Completed in: {round((end-start)*10**3/1000, 5)} Seconds")

    db.close()
    

if __name__=="__main__":
    dumpp()