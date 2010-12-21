#! /usr/bin/python2.6
# -*- coding: utf-8 -*-

import mechanize

def crawl_site(siteurl):
    new_sites = []
    br = mechanize.Browser()
    resp = br.open(siteurl)
    for line in resp.readline():
        mails = find_email(line)
    resp
