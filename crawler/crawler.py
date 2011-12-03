# -*- coding: utf-8 -*- 
import urllib2
import re
import gzip
import StringIO
import time
import random
import MySQLdb
from MySQLdb import OperationalError
from BeautifulSoup import BeautifulSoup
from soupselect import select
import os, sys
cmd_folder = os.path.dirname(os.path.abspath(\
'/home/paul/Documents/FYTproject/segmentation/'))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from segmentation.segLib import segmentate


"""""""""""""""""""""""""""""""""""""""
         CONSTANT DECLARATION
"""""""""""""""""""""""""""""""""""""""
MAXIMUMPAGES=100
DATABASEPATH='../database/'

"""""""""""""""""""""""""""""""""""""""
         VARIABLE DECLARATION
"""""""""""""""""""""""""""""""""""""""
#The start link and rex to check other links of the crawler
#These variables should be merged with Overmind's "CrawlerPolicy"
#startUrl = "http://news.qq.com/a/20110905/000456.htm"
startUrl = "http://news.qq.com/"
rex_exp = 'news.qq.com/a/'
title_selector='#C-Main-Article-QQ .hd h1'
body_selector='#Cnt-Main-Article-QQ p'
pubtime_selector='span.pubTime'

#variables to track the number of pages visited
links=[startUrl]
num_links_visited=0

"""""""""""""""""""""""""""""""""""""""
         FUNCTIONS DEFINITION
"""""""""""""""""""""""""""""""""""""""
def processLink(cur):
    global links
    global num_links_visited
    global MAXIMUMPAGES
    global DATABASEPATH
    #check termination situation of the crawler
    if num_links_visited >= MAXIMUMPAGES:
        print "%d pages collected, the crawler will terminate" % MAXIMUMPAGES
        return 0 

    #get the link that are ready to be visited
    try:
        newurl = links.pop()
    except IndexError:
        print "The list contains unvisited links is empty,",
        print "the crawler will terminate."
        return 0
    num_links_visited += 1
    
    #calculate the time used to process one page
    t0 = time.time() 

    #get the response from the website
    response = urllib2.urlopen(newurl)


    #get the content-encoding info and content type info
    cmz_type = response.headers.get('content-encoding')
    rpe_body = response.read()
    enc_type = response.headers.get('content-type')
    enc_type = enc_type[enc_type.index('=')+1:]
    #convert to "GB2312" to "gbk" in order to let python recognize it
    if enc_type == "GB2312":
        enc_type = "gbk"

    #if the content-encoding is gzip, then unzip the text
    if cmz_type == 'gzip':
        compressedstream = StringIO.StringIO(rpe_body)
        gzipper = gzip.GzipFile(fileobj=compressedstream) 
        rpe_body = gzipper.read()

    #decode the text to utf8
    try:
        rpe_body=rpe_body.decode(enc_type)
    except UnicodeDecodeError:
        print 'Can not detect format %s' % enc_type
    
    soup= BeautifulSoup(rpe_body)

    #use beautifulsoup to search for all the links on the page
    if len(links) < MAXIMUMPAGES:
        anchors = soup.findAll('a',{'href':re.compile(rex_exp)}) 
        for anchor in anchors:
            #finally links contain all the news links on the page
            for attr in anchor.attrs:
                if (attr[0] == u'href'):
                    if len(links) < MAXIMUMPAGES:
                        links.append(attr[1])
                        '''
                        if len(links) >= MAXIMUMPAGES:
                            print "The number of newly grabbed unvisited links",
                            print " exceeds the limit of the crawler. The craw",
                            print "ler will not add more links"
                            break
                        '''

    #get the name of the first level index
    rst = re.search(r'[0-9]{8}',newurl)
    if rst != None:
        dir_name = newurl[rst.start():rst.end()]

    #get article content and save the article to some place
    try:
        title = select(soup,title_selector)[0].text
    except IndexError:
        print "No article title found, this page has no article"
        t1 = time.time() - t0
        print "Time spent on processing page %s is %4.2f second(s)" % (newurl,t1)
        return 1

    f = open('corpus.txt', 'ab')
    title_hash = str(title.__hash__())
    pubtime = select(soup,pubtime_selector)[0].text
    body = []
    for item in select(soup,body_selector):
        if item.findChild() != None:
            continue
        a = segmentate(item.text.encode('utf8'))
        body.append(a.body)
        #save the article to a txt file
        f.write(a.body)

    f.close()


    #save the article to the database
    #first check whether there is a table called "dir_name"
    cur.execute("""SELECT * FROM `DateIndex` WHERE `Date` LIKE '%s'"""%dir_name)
    db_rst=cur.fetchone()
    if (db_rst==None):
        #no table called "dir_name", then: 
        #1.create a new table called "dir_name"
        cur.execute("""
            CREATE TABLE `articles`.`%s` (`daily_number` INT UNSIGNED NOT NULL,
            `title` TEXT NOT NULL,
            `title_hash` TEXT NOT NULL,
            `pub_time` TEXT NOT NULL) ENGINE = MyISAM CHARACTER SET utf8
            COLLATE utf8_bin;
        """%dir_name)
        #2.register this new table to DateIndex
        cur.execute("""
            INSERT INTO `articles`.`DateIndex` (`Date`, `NumOfEntry`) VALUES
            ('%s', '1');
        """%dir_name)
        #3.create a new table for this article 
        try:
            cur.execute("""
                CREATE TABLE  `articles`.`%s` (
                `sentence` MEDIUMTEXT NOT NULL
                ) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_bin;
            """%title_hash)
        except OperationalError:
            return 1

        for sentence in body:
            cur.execute("""
                INSERT INTO `articles`.`%s` (`sentence`) VALUES
                ('%s');
            """%(title_hash,sentence))

        #4.register the information of this artile in table "dir_name"
        cur.execute("""
            INSERT INTO `articles`.`%s` (`daily_number`, `title`, `title_hash`, `pub_time`) VALUES ('1', '%s', '%s', '%s');
        """%(dir_name,title.encode("ascii",'xmlcharrefreplace'),title_hash,pubtime.encode("ascii",'xmlcharrefreplace')))

    else:
        if (db_rst[0] == dir_name):
            #table with same "dir_name" found, then:
            #1. get the "NumOfEntry" of this "dir_name" table in table DateIndex
            cur_num = db_rst[1]
            cur_num=cur_num+1

            #2. update the "NumOfEntry" of this dir_name table in table DateIndex
            cur.execute("""
                UPDATE `articles`.`DateIndex` SET `NumOfEntry` = '%d' WHERE
                `DateIndex`.`Date` = '%s';
            """%(cur_num,dir_name))

            #3.create a new table for this article 
            try:
                cur.execute("""
                    CREATE TABLE  `articles`.`%s` (
                    `sentence` MEDIUMTEXT NOT NULL
                    ) ENGINE = MYISAM CHARACTER SET utf8 COLLATE utf8_bin;
                """%title_hash)
            except OperationalError:
                return 1

            for sentence in body:
                cur.execute("""
                    INSERT INTO `articles`.`%s` (`sentence`) VALUES
                    ('%s');
                """%(title_hash,sentence))
            
            #4.get number of articles in table "dir_name"
            cur.execute("""
                SELECT *  FROM `%s`
            """%dir_name)
            cur_num=c.rowcount
            cur_num=cur_num+1
            #5.register the information of this artile in table "dir_name"
            cur.execute("""
                INSERT INTO `articles`.`%s` (`daily_number`, `title`,
                `title_hash`, `pub_time`) VALUES ('%d', '%s', '%s', '%s');
            """%(dir_name,
            cur_num,
            title.encode("ascii",'xmlcharrefreplace'),
            title_hash,
            pubtime.encode("ascii",'xmlcharrefreplace')))
        else:
            print "Error: %s and %s are not match"%(db_rst[0],dir_name)



         

    t1 = time.time() - t0
    print "Time spent on processing page %s is %4.2f second(s)" % (newurl,t1)
    return 1

"""""""""""""""""""""""""""""""""""""""
     MAIN ENTRY POINT DEFINITION
"""""""""""""""""""""""""""""""""""""""
if __name__ == '__main__':
    print "First Connect to Database.."
    #"~/.my.cnf" is a mysql config file   
    #the connected database must at least have table "DateIndex"
    db=MySQLdb.connect(read_default_file="~/.my.cnf")
    print "Database connection established."
    print "Crawl pages from %s" % startUrl
    c=db.cursor()
    flag=1
    while flag==1:
        flag = processLink(c)
        random.shuffle(links)

#following functions are used to decode xml replaced utf8 characters
#def _callback(matches):
#    id = matches.group(1)
#    try:
#        return unichr(int(id))
#    except:
#        return id
#
#def decode_unicode_references(data):
#    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)
