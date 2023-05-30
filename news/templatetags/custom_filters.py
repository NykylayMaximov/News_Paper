from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


bad_words_list = 'бля блядь бздун бзднуть бздюх блудилище выпердеть высраться выссаться говно говенка говноед говномес ' \
                 'говночист говяга говнюк говняный говна пирога глиномес изговнять гнида гнидас гнидазавр гниданидзе ' \
                 'гондон гондольер даун даунитто дерьмо дерьмодемон дерьмище дрисня дрист дристануть обдристаться ' \
                 'дерьмак дристун дрочить дрочила суходрочер дебил дебилоид дрочка драчун задрот дцпшник елда ' \
                 'елдаклык елдище жопа жопошник залупа залупиться залупинец засеря засранец засрать защеканец ' \
                 'изговнять идиот изосрать курва кретин кретиноид курвырь лезбуха лох минетчица мокрощелка мудак ' \
                 'мудень мудила мудозвон мудацкая мудасраная дерьмопроелдина мусор педрик пердеж пердение пердельник ' \
                 'пердун пидор пидорасина пидорормитна пидорюга педерастер педобратва педигрипал писька писюн ' \
                 'спидозный ссаная спидораковый срать спермер спермобак спермодун срака сракаборец сракалюб срун сука ' \
                 'сучара сучище титьки трипер хер херня херовина хероед охереть хитрожопый хрен моржовый шлюха шлюшидзе'


def censor_word(word):
    count = 0
    new_word = ''
    for i in word:
        if i.isalpha() and count == 1:
            new_word += '*'
        elif i.isalpha():
            new_word += i
            count += 1
        else:
            new_word += i
    return new_word


# проверка переменного на строки я правильно сделал?
# по документации рекомендован вот этот декоратор @stringfilter
# но я не смог проверить правильно ли работает
@register.filter()
@stringfilter
def censor(text):

    text_list = text.split()
    text_list_lower = text.lower().split()
    for i in bad_words_list.split():
        for j in text_list_lower:
            if i in j:
                ind = text_list_lower.index(j)
                text_list[ind] = censor_word(text_list[ind])
    return ' '.join(text_list)