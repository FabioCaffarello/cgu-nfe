HOST = "https://portaltransparencia.gov.br/notas-fiscais/"
PARAMS = "consulta/resultado?paginacaoSimples=true&tamanhoPagina=2&offset="
QUERY = "&direcaoOrdenacao=asc&colunaOrdenacao=municipioFornecedor&de="
FILTER = "&ate="
META = "&colunasSelecionadas=linkDetalhamento%2CorgaoSuperiorDestinatario%2CorgaoDestinatario%2CnomeFornecedor%2CcnpjFornecedor%2CmunicipioFornecedor%2CufFornecedor%2CchaveNotaFiscal%2CvalorNotaFiscal%2CdataEmissao%2CtipoEventoMaisRecente%2Cnumero%2Cserie&_=1657650093440"

NFE_PARAMS = "?ordenarPor=dataEvento&direcao=asc"
PRODUCTS_SERVICES_PARAMS = "itens/resultado?paginacaoSimples=true&tamanhoPagina=15&offset=0&direcaoOrdenacao=asc&colunaOrdenacao=descricao&colunasSelecionadas=numero%2Cdescricao%2CcodigoNcmSh%2CncmSh%2Ccfop%2Cquantidade%2Cunidade%2CvalorUnitario%2Cvalor&idIdentificacao="
PRODUCTS_SERVICES_META = "&_=1657924711124"
EVENTS_PARAMS = "eventos/resultado?paginacaoSimples=true&tamanhoPagina=15&offset=0&direcaoOrdenacao=asc&colunaOrdenacao=dataEvento&colunasSelecionadas=tipoEvento%2CdataEvento%2Cevento%2Cmotivo&idIdentificacao="
EVENTS_META = "&_=1657935295275"

MAX_PROXY_ATTEMPTS = 25
PATH_DEBUG = "tests/response_files/"
