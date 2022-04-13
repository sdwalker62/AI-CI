# There is a problem with Python's coverage analysis tool and SonarQube
# due to slashes being replaced with dots. To fix this we will run this
# script to modify coverage.xml for SonarQube

import os
import sys
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


if os.path.isfile('./coverage.xml'):     
    logging.info('coverage.xml found!')   
    logging.info('attempting correction...')
    
    with open('./new_coverage.xml', 'w') as new_cov, open('./coverage.xml', 'r') as old_cov:
        for line in old_cov.readlines():
            if '.src' in line:
                new_line = line.replace('.src', 'src')
                new_cov.write(new_line)
            else:
                new_cov.write(line)
    
    logging.info('replacement complete!')
    logging.info('switching files...')
    
    os.remove('./coverage.xml')
    os.rename('./new_coverage.xml', './coverage.xml')
    
    logging.info('switch complete!')
else:
    logging.warn('no coverage.xml file found!')
           
                    

