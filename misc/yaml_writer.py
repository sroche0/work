import yaml


def edit_yaml(brand_yaml):
    if not brand_yaml['common'].get('brandable-sidebar-menu-items'):
        brand_yaml['common']['brandable-sidebar-menu-items'] = []
    brand_yaml['ios']['brandable-plists'][0]['Guid'] = 'ios/{}'.format(brand_yaml['ios']['brandable-plists'][0]['Guid'])

    for section in ['common', 'web', 'ios', 'windows8', 'winphone','android']:
        if brand_yaml[section].get('brandable-assets'):
            if section != 'web':
                for index, value in enumerate(brand_yaml[section]['brandable-assets']):
                    brand_yaml[section]['brandable-assets'][index]['Guid'] = '{}/{}'.format(section, value['Guid'])
            else:
                for index, value in enumerate(brand_yaml[section]['brandable-assets']):
                    if '/ios/' in value['Image']:
                        prepend = 'ios/'
                    elif '/android/' in value['Image']:
                        prepend = 'android/'
                    elif '/winphone/' in value['Image']:
                        prepend = 'winphone/'
                    elif '/windows8/' in value['Image']:
                        prepend = 'windows8/'
                    else:
                        prepend = ''

                    if value['Guid'] in ['loginbackground-568@2x.png', 'featured_apps.png', 'logo_tablet.png',
                                         'login_logo_tablet.png', 'login_logo.png', 'logo.png',
                                         'loginbackground-568.png', 'featured_apps_tablet.png', 'loginbackground.png',
                                         'footer_tablet.png', 'loginbackground@2x.png', 'footer.png']:
                        prepend = 'common/'

                    brand_yaml[section]['brandable-assets'][index]['Guid'] = '{}{}'.format(prepend, value['Guid'])

                for index, value in enumerate(brand_yaml[section]['brandable-css']):
                    if '/ios/' in value['Css']:
                        prepend = 'ios/'
                    elif '/android/' in value['Css']:
                        prepend = 'android/'
                    elif '/winphone/' in value['Css']:
                        prepend = 'winphone/'
                    elif '/windows8/' in value['Css']:
                        prepend = 'windows8/'
                    else:
                        prepend = ''

                    brand_yaml[section]['brandable-css'][index]['Guid'] = '{}{}'.format(prepend, value['Guid'])

    return brand_yaml


def write_yaml(file_name, brand_yaml):
    with open(file_name, 'wb') as f:
        for key in ['template', 'version', 'runtime', 'api_version']:
            f.write(yaml.dump({key: brand_yaml[key]}, default_flow_style=False))

        f.write('\n')

        for section in ['common', 'web', 'ios', 'windows8', 'winphone','android']:
            f.write(yaml.dump({section: brand_yaml[section]}, default_flow_style=False))
            f.write('\n')

with open('branding.yaml', 'rb') as f:
    branding_yaml = yaml.load(f)

branding_yaml = edit_yaml(branding_yaml)
write_yaml('branding.yaml', branding_yaml)
