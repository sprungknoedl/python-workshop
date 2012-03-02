#! /usr/bin/python2.6
# -*- coding: utf-8 -*-

import mechanize
import re

br = mechanize.Browser()

def crawl_site(siteurl):
    mails = []
    resp = br.open(siteurl)
    for line in resp:
        for mail in re.findall("\w+@\w+\.\w+", line):
            mails.append(mail)
    for link in br.links():
        mails.extend(crawl_site(link.absolute_url))
    return mails

print crawl_site("http://f0rki.at")
