from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім’я")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Електронна пошта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"
        ordering = ['-created_at']


class Deal(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нова'),
        ('in_progress', 'В процесі'),
        ('won', 'Успішна'),
        ('lost', 'Втрачена'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='deals',
        verbose_name="Клієнт"
    )
    title = models.CharField(max_length=200, verbose_name="Назва угоди")
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сума"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.title} — {self.client.name}"

    class Meta:
        verbose_name = "Угода"
        verbose_name_plural = "Угоди"
        ordering = ['-created_at']


class Note(models.Model):
    deal = models.ForeignKey(
        Deal,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name="Угода"
    )
    text = models.TextField(verbose_name="Текст нотатки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return (
            f"Нотатка до «{self.deal.title}» "
            f"від {self.created_at.strftime('%Y-%m-%d')}"
        )

    class Meta:
        verbose_name = "Нотатка"
        verbose_name_plural = "Нотатки"
        ordering = ['created_at']
