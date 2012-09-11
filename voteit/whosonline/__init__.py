from pyramid.i18n import TranslationStringFactory


PROJECTNAME = "voteit.whosonline"
WhosOnlineMF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.scan(PROJECTNAME)
    #Include translations
    #config.add_translation_dirs('%s:locale/' % PROJECTNAME)
    from .models import ActivityUtil
    util = ActivityUtil()
    config.registry.registerUtility(util)
