# -*- coding: utf-8 -*-
import sys
import traceback
import urllib2

from bs4 import BeautifulSoup

from lib.helper import is_numeric
from lib.logger import logger
from lib.regex_pattern import *

__author__ = 'JP'


class ExtractFacebookProfile:
    def __init__(self):
        self.bf_soup = None
        self.container = None
        self.profile = dict()
        self.base_url = 'https://mbasic.facebook.com'

    @staticmethod
    def extract_value(html, remove_new_line=True):
        result = ''
        try:
            html = html[-1] if isinstance(html, list) else html
            if not remove_new_line:
                html = unicode(html.div).strip()
                html = re.sub(r'<.?(div|p|img|span)[^>]*>', '', html)
            else:
                html = unicode(html.get_text()).strip()
            html = REMOVE_WHITE_SPACE_3.sub(' ', html).strip()
            html = REMOVE_WHITE_SPACE_2.sub(' ', html).strip()
            result = html.encode('ascii', 'xmlcharrefreplace')
        except Exception as e:
            print e
        finally:
            return result

    def get_id(self):
        raw_fb_id = self.bf_soup.find('a', text=PROFILE_ID_CONTAINER)
        if raw_fb_id:
            match_fb_id = PROFILE_ID_PATTERN.search(raw_fb_id['href'])
            if match_fb_id:
                fb_id = match_fb_id.group(2)
                self.profile['id'] = fb_id
            else:
                raw_fb_id = urllib2.unquote(raw_fb_id['href'])
                raw_fb_id = raw_fb_id.replace(self.base_url, '')
                raw_fb_id = raw_fb_id.split(':')
                self.profile['id'] = raw_fb_id[1]

    def get_name(self):
        raw_name = self.bf_soup.find('title')
        if raw_name:
            raw_name = unicode(raw_name.get_text()).strip()
            self.profile['name'] = raw_name.encode('ascii', 'xmlcharrefreplace')

    def get_picture(self):
        raw_picture = self.bf_soup.find('a', href=re.compile(r'photo.php|profile.picture'))
        if raw_picture:
            self.profile['picture'] = raw_picture.find('img')['src']

    def get_living(self):
        places = []
        # other_places = []
        raw_living_data = self.bf_soup.select('#living')
        if raw_living_data:
            raw_living_data = raw_living_data[0]
            raw_living_data = raw_living_data.select('tr')
            if raw_living_data:
                for rn in raw_living_data:
                    tmp = dict()
                    rn_item = rn.select('td')
                    nn_key = self.extract_value(rn_item[0])
                    nn_value = self.extract_value(rn_item[1])
                    if nn_key and nn_value:
                        tmp[nn_key.lower().replace(' ', '_')] = nn_value
                        places.append(tmp)

        if places:
            self.profile['places'] = places

    def get_contact_info(self):
        contact_info = []
        raw_contact = self.bf_soup.select('#contact-info')
        if raw_contact:
            raw_contact = raw_contact[0]
            raw_contact = raw_contact.select('tr')
            if raw_contact:
                for rn in raw_contact:
                    tmp = dict()
                    rn_item = rn.select('td')
                    nn_key = self.extract_value(rn_item[0])
                    nn_value = self.extract_value(rn_item[1])
                    if nn_key and nn_value:
                        nn_key = 'username' if re.search(r'Facebook', nn_key, flags=re.I) else nn_key
                        tmp[nn_key.lower().replace(' ', '_')] = nn_value.lstrip('/')
                        contact_info.append(tmp)

        if contact_info:
            self.profile['contact_info'] = contact_info

    def get_basic_info(self):
        basic_info = []
        raw_basic_info = self.bf_soup.select('#basic-info')
        if raw_basic_info:
            raw_basic_info = raw_basic_info[0]
            raw_basic_info = raw_basic_info.select('tr')
            if raw_basic_info:
                for rn in raw_basic_info:
                    tmp = dict()
                    rn_item = rn.select('td')
                    nn_key = self.extract_value(rn_item[0])
                    nn_value = self.extract_value(rn_item[1])
                    if nn_key and nn_value:
                        tmp[nn_key.lower().replace(' ', '_')] = nn_value
                        basic_info.append(tmp)

        if basic_info:
            self.profile['basic_info'] = basic_info

    def get_works(self):
        result = []
        try:
            container = self.bf_soup.select('#work')
            if container:
                container = container[0]
                container.find('table').decompose()
                raw_works = container.select('.ib')
                if len(raw_works):
                    for works in raw_works:
                        rw = works.select('div')
                        rw = rw[0]
                        rw = rw.select('div')
                        rw = [self.extract_value(r) for r in rw]
                        result.append(rw)
        except Exception as e:
            print logger(message='FBProfile.get_works error: {}'.format(str(e)), level='Error')
        if result:
            self.profile['work'] = result

    def get_education(self):
        result = []
        try:
            container = self.bf_soup.select('#education')
            if container:
                container = container[0]
                container.find('table').decompose()
                # raw_works = container.select('.ib')
                raw_works = container.select('div[id^=u_]')
                if len(raw_works):
                    for works in raw_works:
                        rw = works.select('div')
                        rw = rw[0]
                        rw = rw.select('div')
                        rw = [self.extract_value(r) for r in rw[1:] if self.extract_value(r) not in rw]
                        result.append(rw)
        except Exception as e:
            print logger(message='FBProfile.get_education error: {}'.format(str(e)), level='Error')
        if result:
            self.profile['education'] = result

    def get_nickname(self):
        result = []
        try:
            raw_nicknames = self.bf_soup.select('#nicknames')
            if raw_nicknames:
                raw_nicknames = raw_nicknames[0]
                raw_nicknames = raw_nicknames.select('tr')
                if raw_nicknames:
                    for rn in raw_nicknames:
                        tmp = dict()
                        rn_item = rn.select('td')
                        nn_key = self.extract_value(rn_item[0])
                        nn_value = self.extract_value(rn_item[1])
                        if nn_key and nn_value:
                            tmp[nn_key.lower().replace(' ', '_')] = nn_value
                            result.append(tmp)
        except Exception as e:
            print logger(message='FBProfile.get_nickname error: {}'.format(str(e)), level='Error')
        if result:
            self.profile['nicknames'] = result

    def get_relationship(self):
        raw_relationship = self.bf_soup.select('#relationship')
        if raw_relationship:
            raw_relationship = raw_relationship[0]
            raw_relationship.find('table').decompose()
            self.profile['relationship_status'] = self.extract_value(raw_relationship)

    def get_quotes(self):
        raw_quotes = self.bf_soup.select('#quote')
        if raw_quotes:
            raw_quotes = raw_quotes[0]
            raw_quotes.find('table').decompose()
            self.profile['quotes'] = self.extract_value(raw_quotes, False)

    def get_skills(self):
        raw_skills = self.bf_soup.select('#skills')
        if raw_skills:
            raw_skills = raw_skills[0]
            raw_skills.find('table').decompose()
            self.profile['skills'] = self.extract_value(raw_skills)

    def get_bio(self):
        raw_bio = self.bf_soup.select('#bio')
        if raw_bio:
            raw_bio = raw_bio[0]
            raw_bio.find('table').decompose()
            self.profile['bio'] = self.extract_value(raw_bio, False)

    def get_life_event(self):
        event = dict()
        event_container = None
        try:
            raw = self.bf_soup.select('#root')
            if raw:
                raw = raw[0]
                container = raw.find('div', text=re.compile(r'life event', flags=re.I))
                if container:
                    raw_events_1 = container.parent.parent.parent.parent
                    raw_events_2 = container.parent.parent.parent.parent.parent
                    if raw_events_1 and raw_events_1.name == 'div':
                        event_container = raw_events_1.find_next_sibling()
                    elif raw_events_2 and raw_events_2.name == 'div':
                        event_container = raw_events_2.find_next_sibling()
                    if event_container:
                        r_evs = event_container.select('div div div div')
                        if r_evs:
                            # Get keys
                            for r_ev in r_evs:
                                possible_key = self.extract_value(r_ev)
                                if is_numeric(possible_key) and len(possible_key) == 4:
                                    event[possible_key] = []
                            # Get event items
                            for r_ev in r_evs:
                                event_items = r_ev.select('a')
                                if event_items:
                                    for event_item in event_items:
                                        event_year = event_item.parent.parent.parent.select('div')
                                        if event_year:
                                            event_year = self.extract_value(event_year[0])
                                            if event_year in event:
                                                event_item = self.extract_value(event_item)
                                                if event_item not in event[event_year]:
                                                    event[event_year].append(event_item)
        except Exception as e:
            print logger(message='FBProfile.get_life_event error: {}'.format(str(e)), level='Error')
        if event:
            self.profile['life_events'] = event

    def get_family(self):
        result = []
        try:
            container = self.bf_soup.select('#family')
            if container:
                container = container[0]
                container.find('table').decompose()
                raw_families = container.select('div div')

                if len(raw_families):
                    for raw_family in raw_families:
                        tmp = dict()
                        raw_relation = raw_family.select('h3')
                        raw_name = raw_family.select('h3 a')

                        if raw_name:
                            relation = self.extract_value(raw_relation[-1])
                            name = self.extract_value(raw_name[0])
                            url = raw_name[0]['href']
                            url = '{}{}'.format(self.base_url, url)
                            if not any(d.get('url', None) == url for d in result):
                                tmp['name'] = name
                                tmp['url'] = url
                                tmp['relation'] = relation
                                result.append(tmp)
        except Exception as e:
            print logger(message='FBProfile.get_family error: {}'.format(str(e)), level='Error')
        if result:
            self.profile['family_members'] = result

    def get(self, html_data):
        try:
            self.bf_soup = BeautifulSoup(html_data, 'lxml')
            self.get_id()
            self.get_name()
            self.get_picture()
            self.get_living()
            self.get_contact_info()
            self.get_basic_info()
            self.get_relationship()
            self.get_nickname()
            self.get_works()
            self.get_education()
            self.get_skills()
            self.get_family()
            self.get_life_event()
            self.get_quotes()
            self.get_bio()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()

            err_log = []
            for file_name, line, func, t in traceback.extract_tb(exc_tb):
                file_info = 'File "%s", line %s, in %s\n' % (file_name, line, func)
                file_func = '  %s' % str(t)
                err_log.append((file_info, file_func))
            err_info = 'Error: %s\n' % e

            for i, f in err_log:
                print i, f
            print err_info
        finally:
            return self.profile
