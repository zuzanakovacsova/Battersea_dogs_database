
# Inspired by, code amended to work for SQLalchemy connections: https://www.mysqltutorial.org/python-connecting-mysql-databases/

from configparser import ConfigParser

# Change filename to "teama.teama" or any other user
def read_db_config(filename, section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    
    
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
        
    conn_string = 'mysql+pymysql://'+db['user']+':'+db['password']+'@'+':'.join([db['host'],db['port']])+'/'+db['db']+""
    
    
    return conn_string