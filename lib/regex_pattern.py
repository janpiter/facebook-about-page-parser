import re

__author__ = 'JP'

DAY_OF_WEEK = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
# =================================================================================================
#   FB URL
# -------------------------------------------------------------------------------------------------
REPLACE_COMMENT_URL = re.compile(r'^(.*?\bav=)([0-9]+)(.*?)$', flags=re.I)
# =================================================================================================


# =================================================================================================
#   FB POST
# -------------------------------------------------------------------------------------------------
# Container
POST_CONTAINER = re.compile(r'^year_')

# Post Id
POST_LINK = re.compile(r'Full Story', flags=re.I)
POST_ID_PATTERN_1 = re.compile(r'fbid=([0-9]+)')
POST_FB_ID_PATTERN_1 = re.compile(r'(thid|&id)[=.]([0-9]+)')
POST_AND_FB_ID_PATTERN_1 = re.compile(r'a\.[0-9]+\.[0-9]+\.([0-9]+)/([0-9]+)/')
POST_AND_FB_ID_PATTERN_2 = re.compile(r'(hash=|albums/)([0-9]+)(.*?):thid\.([0-9]+)')

# Post
POST_LIST = re.compile(r'^u_')
POST_SHARED_LINK = re.compile(r'https?://lm.facebook.com')
POST_SHARED_PICTURE_1 = re.compile(r'may contain')
POST_SHARED_PICTURE_2 = re.compile(r'(scontent|external)-(.*?).fbcdn.net')

# Comment
COMMENT_COUNT = re.compile(r'Comments?', flags=re.I)

# Message
EXCLUDE_MESSAGE_1 = re.compile(r'overflow:hidden', flags=re.I)
EXCLUDE_MESSAGE_2 = re.compile(r'See Translation\b', flags=re.I)
EXCLUDE_MESSAGE_3 = re.compile(r'^[0-9]+ stars?$', flags=re.I)

# Types
POST__TYPE_1_PROPIC = re.compile(r'updated? [^ ]+ profile picture', flags=re.I)
POST__TYPE_2_COVER = re.compile(r'updated? [^ ]+ cover photo', flags=re.I)
POST__TYPE_3_ALBUM = re.compile(r'add(ed)? (.*?) to the album', flags=re.I)
POST__TYPE_4_LINK = re.compile(r'shared a link', flags=re.I)
POST__TYPE_5_CHECK_IN = re.compile(r' is at ', flags=re.I)
POST__TYPE_6_SHARED_VIDEO = re.compile(r'shared (.*?) video', flags=re.I)

# Username
POST_USERNAME = re.compile(r'^/([^?]+)\?')
# =================================================================================================


# =================================================================================================
#   FB COMMENT
# -------------------------------------------------------------------------------------------------
# Comment Id
COMMENT_POST_LINK = re.compile(r'\bReply\b', flags=re.I)
COMMENT_POST_LINK_2 = re.compile(r'\b(un)?like\b', flags=re.I)
COMMENT_POST_LINK_3 = re.compile(r'\bReport\b', flags=re.I)
COMMENT_POST_LINK_PATTERN = re.compile(r'comment_form_(.*)')
COMMENT_POST_LINK_PATTERN_2 = re.compile(r'like_comment_id=([0-9]+)(.*?)ft_ent_identifier=([0-9]+)')

# Username
COMMENT_FB_URL_CLEANSING = re.compile(r'[&?](refid=.*|rc=p|__tn__=.*)')

# User ID
COMMENT_FB_ID = re.compile(r'profile.php\?id=([0-9]+)')
# =================================================================================================


# =================================================================================================
#   FB PROFILE
# -------------------------------------------------------------------------------------------------
# FB Id
PROFILE_ID_CONTAINER = re.compile(r'^(More$|Block this|Timeline)', flags=re.I)
PROFILE_ID_PATTERN = re.compile(r'(owner_id|bid)=([0-9]+)', flags=re.I)
# =================================================================================================


# =================================================================================================
#   OTHERS
# -------------------------------------------------------------------------------------------------
NUMERIC = re.compile(r'[0-9]+')
NON_NUMERIC = re.compile(r'[^0-9]+')
REMOVE_HTML_TAG = re.compile(r'<[^>]+>')
REPLACE_TAG_1 = re.compile(r'<(br/?.?|/p|/h3|/abbr|/div)>')
REMOVE_WHITE_SPACE = re.compile(r'&[^; ]+;')
REMOVE_WHITE_SPACE_2 = re.compile(r'[ ]+')
REMOVE_WHITE_SPACE_3 = re.compile(r'\n+')
DATE_PATTERN_1 = re.compile(r'([0-9]+) mins?')
DATE_PATTERN_2 = re.compile(r'just now', flags=re.I)
DATE_PATTERN_3 = re.compile(r'([0-9]+) hrs?')
DATE_PATTERN_4 = re.compile(r'\byesterday at (.*)', flags=re.I)
DAY_OF_WEEK_PATTERN = re.compile(r'{}'.format('|'.join(DAY_OF_WEEK)), flags=re.I)
# =================================================================================================
