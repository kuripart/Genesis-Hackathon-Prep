from configparser import ConfigParser

# sample parser
parser_ = [('host', 'localhost'), ('database', 'hackathon_01_db'), ('user', 'kuri'), ('password', 'hack19')]


def test_config(*args, **kwargs):
    print(kwargs)


def config(file='database.ini', section='postgresql'):
    db = {}
    parser = ConfigParser()
    parsed_file = parser.read(file)
    # print(parsed_file)
    # print(parser)

    if parser.has_section(section):
        params = parser.items(section)
        # print(params)
        for param in params:
            db[param[0]] = param[1]
    return db


if __name__ == '__main__':
    db_params = config()
    test_config(**db_params)

