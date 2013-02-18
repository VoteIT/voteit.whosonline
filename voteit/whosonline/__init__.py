from pyramid.i18n import TranslationStringFactory


PROJECTNAME = "voteit.whosonline"
WhosOnlineMF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.scan(PROJECTNAME)
    #Include translations
    config.add_translation_dirs('%s:locale/' % PROJECTNAME)
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('whosonline_static', '%s:static' % PROJECTNAME, cache_max_age = cache_ttl_seconds)
    from .models import ActivityUtil
    util = ActivityUtil()
    config.registry.registerUtility(util)
