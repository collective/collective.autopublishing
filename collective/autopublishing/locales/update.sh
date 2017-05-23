domain='collective.autopublishing'

# Synchronise the templates and scripts with the .pot file for collective.autopublishing domain.
i18ndude rebuild-pot --pot ./$domain.pot --create $domain ../
i18ndude sync --pot ./$domain.pot ./*/LC_MESSAGES/$domain.po

# Synchronise the collective.autopublishing's pot file (Used for the workflows)
#i18ndude rebuild-pot --pot ./plone.pot --merge ./plone-manual.pot --create plone ../profiles
i18ndude rebuild-pot --pot ./plone.pot --create plone ../profiles
i18ndude sync --pot plone.pot ./*/*/plone.po

WARNINGS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find . -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings (possibly missing i18n markup)"
echo "There are $ERRORS errors (almost definitely missing i18n markup)"
echo "There are $FATAL fatal errors (template could not be parsed, eg. if its not html)"
echo "For more details, run 'find . -name \"*pt\" | xargs i18ndude find-untranslated' or"
echo "Look the rebuild i18n log generate for this script called 'rebuild_i18n.log' on locales dir"

rm ./rebuild_i18n.log

touch ./rebuild_i18n.log

find ../ -name "*pt" | xargs i18ndude find-untranslated > ./rebuild_i18n.log
