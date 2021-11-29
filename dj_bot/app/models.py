from django.db import models


class Event(models.Model):

    price = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Цена билета")
    slug = models.SlugField(
        unique=True,
        verbose_name="Slug-name 'Должно быть уникальным, состоять из латинских букв и цифр, без пробелов'")
    count_tickets = models.IntegerField(verbose_name="Количество билетов на игру")
    busy_tickets = models.IntegerField(default=0, verbose_name="Занято билетов")
    date = models.DateTimeField(verbose_name="Дата события")
    bank = models.DecimalField(default=0, max_digits=9, decimal_places=6, verbose_name="Банк")

    def __str__(self):
        return f"№ {self.pk} | дата {self.date.strftime('%d-%m-%Y %H:%M')}"

    class Meta:
        verbose_name = "События"
        verbose_name_plural = "События"


class Ticket(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Событие")
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Билеты"
        verbose_name_plural = "Билеты"


class UserProfile(models.Model):

    id_tg = models.BigIntegerField(unique=True, null=False, verbose_name="ID Пользователя телеграм")
    user_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Имя пользователя")
    purse = models.CharField(max_length=255, null=True, blank=True, verbose_name="Кошелек пользователя")
    account_amount = models.DecimalField(max_digits=9, decimal_places=6, default=0, verbose_name="Сумма на счету")

    def __str__(self):
        return f"Пользователь : {self.user_name}"

    class Meta:
        verbose_name = f"Пользователи"
        verbose_name_plural = f"Пользователи"


class Balance(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Пользователь")
    get_sum = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Запоршеная сумма")
    user_purse = models.CharField(max_length=255, blank=True, null=True, verbose_name="Кошелек пользователя")
    confirm_transaction = models.ImageField(
        upload_to="media/Y%/m%/d%/", blank=True, null=True, verbose_name="Подтверждение транзакции"
    )
    inquire_process = models.BooleanField(default=False, verbose_name="Оплачено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата запорса")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновление запроса")

    class Meta:
        verbose_name = "Запорсы на вывод средств"
        verbose_name_plural = "Запорсы на вывод средств"

    def __str__(self):
        return f" {self.user},  Запршиваемая сумма {self.get_sum}"


class ArchiveGame(models.Model):

    id_game = models.CharField(max_length=255, verbose_name="ID прошедшей игры")
    date_game = models.DateTimeField(verbose_name="Дата игры")
    count_players = models.IntegerField(verbose_name="Количество игроков")
    players = models.ManyToManyField(UserProfile, verbose_name="Игроки", related_name='players')
    bank = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Разыгрываемая сумма")
    winner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Победитель")
    random_num = models.IntegerField(verbose_name="Случайное число")
