import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader
from scrapy.item import Item
from datetime import datetime

from .spiders import parser


class CguNfeLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def add_fields(self, fields):
        for key, value in fields.items():
            globals()[f"{key}"] = value
        self.add_value('chaveDeAcesso', chaveDeAcesso)
        self.add_value('valorTotalDaNotaFiscalR', valorTotalDaNotaFiscalR)
        self.add_value('modelo', parser.normalize_text(modelo))
        self.add_value('serie', serie)
        self.add_value('numero', numero)
        self.add_value('dataDeEmissao', dataDeEmissao)
        self.add_value('naturezaDaOperacao', naturezaDaOperacao)
        self.add_value('situacao', situacao)
        self.add_value('dataDaUltimaModificacao', dataDaUltimaModificacao)
        self.add_value('destinatario', destinatario)
        self.add_value('emitente', emitente)
        self.add_value('produtosServicos', produtosServicos)
        self.add_value('eventos', eventos)
        self.add_value('event_timestamp', datetime.now())
        pass


class CguNfeItem(Item):
    chaveDeAcesso = scrapy.Field()
    valorTotalDaNotaFiscalR = scrapy.Field()
    modelo = scrapy.Field()
    serie = scrapy.Field()
    numero = scrapy.Field()
    dataDeEmissao = scrapy.Field()
    naturezaDaOperacao = scrapy.Field()
    situacao = scrapy.Field()
    dataDaUltimaModificacao = scrapy.Field()
    destinatario = scrapy.Field()
    emitente = scrapy.Field()
    produtosServicos = scrapy.Field()
    eventos = scrapy.Field()
    event_timestamp = scrapy.Field()
    pass
