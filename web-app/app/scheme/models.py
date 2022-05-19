from django.db import models


class Therm(models.Model):
    title = models.CharField('Термин', max_length=100)
    body = models.TextField('Определение')
    image = models.ImageField('Рисунок', null=True, upload_to='scheme/')
    mark = models.CharField('Обозначение', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Термин'
        verbose_name_plural = 'Термины'


class Connection(models.Model):
    title = models.CharField('Связь', max_length=100)
    body = models.TextField('Определение')
    image = models.ImageField('Рисунок', upload_to='scheme/connection')
    mark = models.CharField('Обозначение', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'


class XmlFile(models.Model):
    title = models.CharField('Имя файла', max_length=100)
    file = models.FileField('Файл', upload_to='scheme/xml')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Xml файл'
        verbose_name_plural = 'Xml файлы'


class RelationshipsTherm(models.Model):
    therm_id = models.IntegerField('первый термин')
    title = models.CharField('первый термин', max_length=100)
    web = models.CharField('ссылка', max_length=100)
    therm_title = models.CharField('второй термин', max_length=100)
    connection = models.CharField('Связь терминов', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Связь терминов'
        verbose_name_plural = 'Связи терминов'


class Mierda(models.Model):
    title = models.CharField('термин', max_length=100)
    body = models.TextField('Определение')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/scheme/relationships_terms'

    class Meta:
        verbose_name = 'определение'
        verbose_name_plural = 'определения'
