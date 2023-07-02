# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import mail_managers, send_mail
# from .models import Post, PostCategory, SubscribeCategory
#
#
# @receiver(post_save, sender=PostCategory)
# def notify_managers_appointment(sender, instance, created, **kwargs):
#     category_list = instance.category
#     post_id = instance.post_id
    # user_id_list = []
    # user_subscriber_list = []
    # user_email_dict = {}
    #
    # for category in category_list:
    #     PostCategory.objects.create(post_id=post_id, category_id=category)
    #     user_id_list += SubscribeCategory.objects.filter(category_id=category).values('subscriber__id')
    #
    # for user in user_id_list:
    #     if user['subscriber__id'] not in user_subscriber_list:
    #         user_subscriber_list.append(user['subscriber__id'])
    #
    # for id in user_subscriber_list:
    #     subscribe_user = User.objects.get(pk=id)
    #     user_email_dict[subscribe_user.username] = subscribe_user.email
    #
    # print(user_id_list)
    # print(user_subscriber_list)
    # print(user_email_dict)

    # if created:
    #     subject = instance.title
    # else:
    #     subject = f'Этот пост был изменен: {instance.title}'


    # send_mail(
    #     subject=f'{post_id}',
    #     message=f'{category_list}',
    #     from_email='nick.max89@gmail.com',
    #     recipient_list=['nick.max@mail.ru']
    # )

    #   html_content = render_to_string('post_send_email.html', {'post': post, 'user_name': user_name})
    #   msg = EmailMultiAlternatives(
    #              subject=post.title,
    #                 from_email='nick.max89@gmail.com',
    #                 to=[email]
    #             )
    #             msg.attach_alternative(html_content, 'text/html')
    #             msg.send()
