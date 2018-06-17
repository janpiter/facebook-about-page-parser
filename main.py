import os
import json
from facebook_profile_extractor import ExtractFacebookProfile

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':

    efp = ExtractFacebookProfile()
    sample_directory = os.listdir('{}/tests'.format(CURRENT_DIR))

    for sample_file in sample_directory:
        if sample_file.endswith('.html'):
            print '=' * 100
            print 'Parsing file {}:'.format(sample_file)
            print '-' * 100
            sample_data = open('{}/tests/{}'.format(CURRENT_DIR, sample_file))
            result = efp.get(sample_data)
            if result:
                print json.dumps(result, indent=4)
            print '=' * 100
            print
