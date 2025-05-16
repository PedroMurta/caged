<h1 align='center'> 📘 Análise da Escassez de Motoristas no Brasil</h1>

## 🧭 Introdução

  <p>  A escassez de motoristas profissionais no Brasil representa um desafio crescente para o setor de transporte e logística. A predominância do transporte rodoviário na movimentação de cargas e pessoas no país torna essa categoria essencial para o funcionamento da
  economia.</p>

Este estudo visa analisar, por meio dos dados abertos do CAGED (Cadastro Geral de Empregados e Desempregados), as principais tendências trabalhistas associadas aos motoristas formais do setor de transporte (Setor H - Transporte, Armazenagem e Correios), com destaque para os motoristas em geral e motoristas de caminhão.


---

## 🧾 Fonte dos Dados

Os dados utilizados neste relatório foram extraídos dos dados abertos do **CAGED**, segmentados especificamente para o **setor H** (Transporte, Armazenagem e Correio), conforme o Painel CNT do Transporte. O período analisado abrange **Janeiro de 2010 a Fevereiro de 2025**.

- Dados de 2020 até 2025: obtidos via FTP do Novo CAGED  - (**ftp://ftp.mtps.gov.br/pdet/microdados**)
- Dados de 2010 a 2019: obtidos majoritariamente via FTP do CAGED Antigo; dados corrompidos foram completados com uma base alternativa.

---

## 🚛 CBOs Considerados – Motoristas

### CBOs Específicos

<div align="center">

| Código | Descrição                                              |
|--------|--------------------------------------------------------|
| 782310 | Motorista de carro de passeio                          |
| 782320 | Motorista de táxi                                      |
| 782405 | Motorista de ônibus urbano                             |
| 782410 | Motorista de ônibus rodoviário                         |
| 782415 | Motorista de ônibus escolar                            |
| 782510 | Motorista de caminhão – rotas regionais/internacionais |
| 782515 | Motorista de caminhão-guincho pesado com munk          |
</div>

### Grupos Ocupacionais

| Código | Descrição                                                       |
|--------|-----------------------------------------------------------------|
| 7823   | Motoristas de veículos de passageiros (grupo amplo)            |
| 7824   | Motoristas de veículos de carga (grupo amplo)                  |
| 7825   | Motoristas de transporte de cargas e passageiros               |
| 7821   | Condutores de veículos a motor                                 |
| 7822   | Motorista de veículo de pequeno porte                          |


> _Como os dados são voláteis e sempre passam por revisões e variações pequenas ao longo do tempo e o foco está em analisar tendências, os dados dessa análise foram arredondados para melhor visualização sem prejuízo à tendência geral._

---

<h2 align='center'> 👥 Perfil Sociodemográfico </h2>

### Escolaridade

- 📘 **Predominância de Ensino Médio Completo** desde 2011.
- Em 2010, o grau mais comum era o **Ensino Fundamental Completo**.
- Isso mostra uma exigência crescente de escolaridade no setor.


### Gênero

- 👨 **Predomínio esmagador do sexo masculino** em todos os anos da série histórica (mais de 90%).
- O setor ainda carece de políticas mais consistentes de **inclusão de mulheres**.


---
<h2 align='center'> 🚛 Foco: Motorista de Caminhão – Rotas Regionais e Internacionais. <br><i>CBO 7825-10</i></h2>

| ano | salario medio | idade media | total admissoes | total demissoes | saldo total | escolaridade mais comum | etnia mais comum | sexo mais comum | salario minimo | saldo acumulado | poder de compra |
|-----|---------------|-------------|------------------|------------------|-------------|--------------------------|-------------------|------------------|-----------------|------------------|-----------------|
| 2010 | 1.033,68     | 37.27       | 179.600          | 157.700          | 21.900      | Fundamental Completo     | Branca            | Homem            | 510.00          | 21.900          | 2.03            |
| 2011 | 1.132,92     | 37.35       | 201.100          | 183.900          | 17.200      | Médio Completo           | Branca            | Homem            | 545.00          | 39.100          | 2.08            |
| 2012 | 1.228,29     | 37.48       | 204.600          | 191.700          | 12.800      | Médio Completo           | Branca            | Homem            | 622.00          | 51.900          | 1.97            |
| 2013 | 1.340,21     | 37.75       | 217.400          | 203.300          | 14.000      | Médio Completo           | Branca            | Homem            | 678.00          | 65.900          | 1.98            |
| 2014 | 1.457,18     | 38.04       | 217.100          | 215.800          | 1.400       | Médio Completo           | Branca            | Homem            | 724.00          | 67.300          | 2.01            |
| 2015 | 1.559,18     | 38.58       | 178.300          | 192.400          | -14.100     | Médio Completo           | Branca            | Homem            | 788.00          | 53.200          | 1.98            |
| 2016 | 1.692,33     | 39.41       | 147.100          | 168.100          | -21.000     | Médio Completo           | Branca            | Homem            | 880.00          | 32.200          | 1.92            |
| 2017 | 1.805,08     | 39.94       | 138.100          | 135.300          | 2.700       | Médio Completo           | Branca            | Homem            | 937.00          | 34.900          | 1.93            |
| 2018 | 1.889,66     | 40.39       | 136.700          | 120.700          | 15.900      | Médio Completo           | Branca            | Homem            | 954.00          | 50.800          | 1.98            |
| 2019 | 1.948,15     | 40.64       | 164.900          | 147.100          | 17.800      | Médio Completo           | Branca            | Homem            | 998.00          | 68.600          | 1.95            |
| 2020 | 2.167,25     | 40.87       | 204.000          | 188.400          | 15.600      | Médio Completo           | Parda             | Homem            | 1.045,00       | 84.200          | 2.07            |
| 2021 | 2.236,41     | 40.83       | 257.400          | 227.600          | 29.700      | Médio Completo           | Parda             | Homem            | 1.100,00       | 113.900         | 2.03            |
| 2022 | 2.298,77     | 40.91       | 272.600          | 244.100          | 28.500      | Médio Completo           | Parda             | Homem            | 1.212,00       | 142.400         | 1.90            |
| 2023 | 2.556,28     | 40.84       | 288.200          | 271.000          | 17.200      | Médio Completo           | Parda             | Homem            | 1.320,00       | 159.600         | 1.94            |
| 2024 | 2.580,82     | 40.95       | 312.900          | 301.300          | 11.600      | Médio Completo           | Parda             | Homem            | 1.412,00       | 171.200         | 1.83            |
| 2025 | 2.803,12     | 41.01       | 53.000           | 51.400           | 1.600       | Médio Completo           | Parda             | Homem            | 1.518,00       | 172.800         | 1.85            |



## Distribuição de Admissões por Faixa Etária – Caminhoneiros  

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <div style="max-width: 880px;">
    <h4> Distribuição de Admissões por Faixa Etária</h4>
    <ul>
      <li><strong>Forte queda na entrada de jovens: </strong>  A faixa 18–24 anos caiu de 6,91% em 2010 para 4,15% em 2024, indicando redução no interesse ou acesso dos jovens à profissão de caminhoneiro.</li>
      <li><strong>Faixa 30–39 continua predominante:</strong> é a faixa com maior volume de admissões, mas sua participação vem diminuindo: de 40,39% em 2014 para 30,70% em 2024, reforçando a tendência de envelhecimento do setor.</li>
      <li><strong>Avanço das faixas mais velhas:</strong> As faixas 50–64 anos e 65+ cresceram bastante, com a de 50–64 saltando de 11,70% em 2010 para 19,93% em 2024. Isso mostra uma dependência crescente de trabalhadores mais velhos, o que pode gerar problemas de reposição no médio prazo.</li>
    </ul>
    <p> O mercado de motoristas está envelhecendo, com menos jovens ingressando e aumento da contratação de faixas etárias mais avançadas, apontando para um risco estrutural de escassez de mão de obra no futuro próximo..</p>
  </div>
  <img src="distribuicao_etaria_admissao_grafico.png" style="width: 880px;">
</div>

 ----------------
## Evolução do Saldo de Caminhoneiros por Ano 

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <img src="evolucao_saldo_ano.png" style="width: 800px; margin-right: 30px;">
  <div style="max-width: 880px;">
    <h4> Evolução do Saldo de Caminhoneiros por Ano (2010–2024)</h4>
    <ul>
      <li><strong>Crise profunda (2015–2016):</strong>O saldo despenca, com –14.100 em 2015 e –21.000 em 2016, refletindo os efeitos da recessão econômica brasileira e início da saída de motoristas do mercado.</li>
      <li><strong>Recuperação parcial (2017–2021):</strong>O saldo retorna ao positivo, mas sem atingir os patamares do início da série. O setor retoma contratações, mas em menor escala.</li>
      <li><strong>Pico de recuperação (2022):</strong>O saldo atinge o maior valor da série: 29.700, possivelmente impulsionado pela retomada econômica pós-pandemia e pelo aumento da demanda por entregas e transporte de mercadorias, impulsionado pelo crescimento do e-commerce e serviços de delivery.</li>
    </ul>
  </div>
</div>

-------------------------------
## 📈 Poder de Compra – Motoristas de Caminhão 

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">  
  <div style="max-width: 880px; font-family: Arial, sans-serif;">
    <h4> Poder de Compra – Motoristas de Caminhão</h4>
  <p>
      Este gráfico apresenta a evolução do poder de compra ao longo do tempo
      
  </p>

  <ul>
      <li>📉 <strong>Defasagem salarial:</strong> Apesar do aumento nominal dos salários, o poder de compra caiu, indicando que os reajustes não acompanham o salário mínimo. Isso sugere perda de atratividade econômica da profissão.</li>
      <li>📊 <strong>Tendência clara de envelhecimento:</strong> A idade média aumentou de 37,27 anos (2010) para 40,95 anos (2024). Isso indica uma menor entrada de jovens no setor.</li>
      
  </ul>
<p>
Esses efeitos distorcem o valor médio, sem necessariamente significar ganho real de poder de compra para a maioria dos trabalhadores
</p>
  </div>
  <img src="evolucao_idade_poder_compra.png" style="width: 880px; margin-right: 30px;">
</div>


------------------------------------
## 📈 Evolução Percentual – Motoristas de Caminhão

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <img src="Evolucao_idade_caminhoneiros.png" style="width: 880px; margin-right: 30px;">
  <div style="max-width: 600px; font-family: Arial, sans-serif;">
    <h4>📈 Evolução Percentual da Idade Média – Motoristas de Caminhão</h4>
   <p>
      Este gráfico apresenta a variação percentual anual da <strong>idade média</strong> dos motoristas de caminhão, comparando cada ano com o anterior.
    </p>
  <ul>
      <li>📉 <strong>Envelhecimento constante: </strong>a média de idade aumentou de forma contínua ao longo dos anos, passando de 37,27 em 2010 para 41,02 em 2024. com crescimento praticamente em todos os anos/li>
      <li>📊 <strong>Pico em 2015 e 2016:</strong> Os maiores aumentos percentuais ocorreram entre 2015 e 2016 (+2,15%) e 2014 e 2015 (+1,42%), sugerindo forte envelhecimento no período pós-crise econômica.</li>
      <li>😷 <strong>Efeitos da pandemia em 2020:</strong> o crescimento da idade média desacelera, mas continua. As únicas quedas foram em 2021 (–0,10%) e 2022 (–0,17%), indicando pequenas flutuações.</li>
    </ul>
    <p>
      O setor tem envelhecido de forma consistente, reforçando a tese de que há uma baixa renovação geracional entre os motoristas profissionais.</p>
  </div>
</div>


----------------------------------------------------------------------------

---
## 📍 Motoristas em Geral

| ano  | salario medio | idade media | total admissoes | total demissoes | saldo total | escolaridade mais comum | etnia mais comum | sexo mais comum | salario minimo | saldo acumulado | poder de compra |
|------|----------------|--------------|------------------|------------------|--------------|--------------------------|-------------------|------------------|-----------------|------------------|---------------|
| 2010 | 1.056,26       | 37.50        | 287.100          | 262.000          | 25.100       | Fundamental Completo     | Branca            | Homem            | 510,00          | 25.100           | 2.07          |
| 2011 | 1.156,26       | 37.55        | 322.700          | 298.600          | 24.100       | Médio Completo           | Branca            | Homem            | 545,00          | 49.200           | 2.12          |
| 2012 | 1.251,46       | 37.69        | 325.500          | 311.700          | 13.800       | Médio Completo           | Branca            | Homem            | 622,00          | 63.000           | 2.01          |
| 2013 | 1.368,87       | 38.00        | 347.200          | 332.300          | 14.900       | Médio Completo           | Branca            | Homem            | 678,00          | 77.900           | 2.02          |
| 2014 | 1.487,06       | 38.27        | 351.300          | 347.200          | 4.100        | Médio Completo           | Branca            | Homem            | 724,00          | 82.000           | 2.05          |
| 2015 | 1.595,83       | 38.87        | 290.400          | 315.200          | -24.800      | Médio Completo           | Branca            | Homem            | 788,00          | 57.200           | 2.03          |
| 2016 | 1.722,15       | 39.67        | 234.500          | 273.400          | -38.900      | Médio Completo           | Branca            | Homem            | 880,00          | 18.300           | 1.96          |
| 2017 | 1.827,77       | 40.22        | 211.800          | 219.300          | -7.500       | Médio Completo           | Branca            | Homem            | 937,00          | 10.800           | 1.95          |
| 2018 | 1.908,71       | 40.71        | 203.000          | 192.000          | 11.100       | Médio Completo           | Branca            | Homem            | 954,00          | 21.900           | 2.00          |
| 2019 | 1.968,75       | 40.96        | 240.900          | 226.600          | 14.200       | Médio Completo           | Branca            | Homem            | 998,00          | 36.100           | 1.97          |
| 2020 | 2.225,00       | 41.49        | 272.300          | 300.600          | -28.300      | Médio Completo           | Parda             | Homem            | 1.045,00        | 7.800            | 2.13          |
| 2021 | 2.472,99       | 41.30        | 359.500          | 330.900          | 28.500       | Médio Completo           | Parda             | Homem            | 1.100,00        | 36.300           | 2.25          |
| 2022 | 2.341,22       | 41.37        | 393.300          | 352.700          | 40.600       | Médio Completo           | Parda             | Homem            | 1.212,00        | 76.900           | 1.93          |
| 2023 | 2.577,18       | 41.30        | 412.300          | 383.400          | 28.900       | Médio Completo           | Parda             | Homem            | 1.320,00        | 105.800          | 1.95          |
| 2024 | 2.607,07       | 41.41        | 441.400          | 424.300          | 17.100       | Médio Completo           | Parda             | Homem            | 1.412,00        | 122.900          | 1.85          |
| 2025 | 2.751,51       | 41.58        | 76.900           | 72.300           | 4.600        | Médio Completo           | Parda             | Homem            | 1.518,00        | 127.500          | 1.81          |



## Distribuição de Admissões por Faixa Etária – Motoristas

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <div style="max-width: 880px;">
    <h4> Distribuição de Admissões por Faixa Etária</h4>
    <ul>
      <li><strong>Queda acentuada na contratação de jovens: </strong> A faixa 18–24 anos caiu de 6,50% em 2010 para 4,09% em 2024, evidenciando um desinteresse ou dificuldade de inserção dos mais jovens na profissão de motorista.</li>
      <li><strong>Faixa 30–39 continua predominante:</strong> é a faixa com maior volume de admissões, mas sua participação vem diminuindo: de 40,39% em 2014 para 30,70% em 2024, reforçando a tendência de envelhecimento do setor.</li>
      <li><strong>Avanço das faixas mais velhas:</strong> As faixas 50–64 anos e 65+ cresceram bastante, com a de 50–64 saltando de 11,70% em 2010 para 19,93% em 2024. Isso mostra uma dependência crescente de trabalhadores mais velhos, o que pode gerar problemas de reposição no médio prazo.</li>
    </ul>
    <p> O mercado de motoristas está envelhecendo, com menos jovens ingressando e aumento da contratação de faixas etárias mais avançadas, apontando para um risco estrutural de escassez de mão de obra no futuro próximo.</p>
  </div>
  <img src="distribuicao_etaria_admissao_grafico.png" style="width: 880px;">
</div>


 ----------------
## Evolução do Saldo de Motoristas

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <img src="distribuicao_admissao_faixa_etaria_grafico_motoristas.png" style="width: 800px; margin-right: 30px;">
  <div style="max-width: 880px;">
    <h4> Evolução do Saldo de Caminhoneiros por Ano (2010–2024)</h4>
    <ul>
      <li><strong>Crise profunda (2015–2016):</strong>O saldo de empregos despencou, chegando a –27.150 em 2015 e –39.950 em 2016, o pior da série. Esse período coincide com a recessão econômica nacional.</li>
      <li><strong>Recuperação gradual (2017–2019):</strong> O saldo volta ao positivo de forma modesta, indicando uma tentativa de reestruturação do setor.</li>
      <li><strong>Novo baque em 2020 (–29.970):</strong>Mesmo com aumento da demanda logística pela pandemia, o saldo foi fortemente negativo, possivelmente devido à paralisação de serviços presenciais, incertezas econômicas e mudanças operacionais.</li>
      <li><strong>Pico de retomada em 2022: </strong> O setor registrou o maior saldo positivo da série (39.910), refletindo a forte demanda pós-pandemia, com crescimento do e-commerce e da atividade econômica.</li>
      <li><strong>Queda recente: </strong> Em 2023 (29.470) e 2024 (17.690), o saldo caiu, sugerindo desaceleração ou dificuldades de contratação e reposição da mão de obra.</li>
    </ul>
    <p>  O setor de motoristas apresenta ciclos de alta sensibilidade à economia, com fortes quedas em momentos de crise e retomadas expressivas pós-recuperação. A dificuldade de reposição, especialmente entre jovens, agrava os desafios estruturais.</p>
  </div>
</div>

-------------------------------
## 📈 Poder de Compra – Motoristas

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">  
  <div style="max-width: 880px; font-family: Arial, sans-serif;">
    <h4> Poder de Compra – Motoristas de Caminhão</h4>
  <p>
      Este gráfico apresenta a evolução do poder de compra ao longo do tempo
      
  </p>

  <ul>
      <li>📉 <strong>Envelhecimento da categoria:</strong> A idade média dos motoristas cresceu de 37,48 anos em 2010 para 41,37 anos em 2024, evidenciando a baixa renovação geracional na profissão.</li>
      <li>📊 <strong>Poder de compra em queda:</strong> Após um pico em 2021 (2,2 salários mínimos), o poder de compra despencou para 1,84 em 2024, atingindo o pior patamar da série.</li>
      <li>📊 <strong>Descolamento entre idade e remuneração:</strong> Mesmo com trabalhadores mais experientes e envelhecidos, o poder de compra não acompanhou esse avanço, indicando valorização salarial insuficiente frente à inflação.</li>
      
  </ul>
<p>
 O gráfico reforça o cenário preocupante de um setor que envelhece sem atrair jovens e que perdeu atratividade econômica, tornando mais difícil reverter a escassez de motoristas no longo prazo.</p>
  </div>
  <img src="idade_media_poder_compra_motoristas.png" style="width: 880px; margin-right: 30px;">
</div>


------------------------------------
## 📈 Evolução Percentual – Motoristas

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <img src="evolucao_idade_media_motoristas.png" style="width: 880px; margin-right: 30px;">
  <div style="max-width: 600px; font-family: Arial, sans-serif;">
    <h4>📈 Evolução Percentual da Idade Média – Motoristas de Caminhão</h4>
   <p>
      Este gráfico apresenta a variação percentual anual da <strong>idade média</strong> dos motoristas de caminhão, comparando cada ano com o anterior.
    </p>
  <ul>
      <li>📉 <strong>Envelhecimento Contínuo: </strong>A idade média dos motoristas aumentou de 37,48 em 2010 para 41,56 em 2024, um crescimento de mais de 4 anos em 14 anos, indicando menor entrada de jovens e permanência de trabalhadores mais velhos.</li>
      <li>📊 <strong>Pico em 2014 e 2017:</strong> Destaque para os anos de 2015 (+1,54%) e 2016 (+2,08%), período de crise econômica, quando a contratação de jovens caiu e o setor passou a depender mais de profissionais experientes.</li>
      <li>😷 <strong>Estabilização recente:</strong> De 2021 a 2023 houve pequenas quedas ou variações discretas (–0,43% em 2021 e –0,19% em 2023), mas a idade voltou a subir em 2024 (+0,46%).</li>
    </ul>
    <p>
      O gráfico evidencia uma tendência clara e consistente de envelhecimento entre os motoristas, o que, somado à baixa renovação etária, representa um desafio crescente para o setor de transporte no Brasil.</p>
  </div>
</div>





---


### 🔍 Limitações

- **CAGED não capta autônomos nem MEIs**, o que deixa de fora uma parcela significativa da força de trabalho, especialmente:
  - Motoristas de aplicativos
  - Caminhoneiros independentes
  - Profissionais terceirizados via frota agregada

- **Ausência de dados sobre jornada de trabalho**, tempo médio em rodovias, pausas ou condições de saúde.


## 🚧 Fatores Qualitativos da Profissão

- 💰 **Remuneração instável:** [Salários variáveis e muitas vezes insuficientes frente às exigências do trabalho.](https://estradao.estadao.com.br/caminhoes/cnt-e-governo-criam-programa-para-diminuir-falta-de-caminhoneiros-brasil/)
- 🕐 **Jornada exaustiva:** [Longas horas de trabalho com pouco suporte na estrada.](https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2023/novembro/operacao-jornada-legal-flagra-motoristas-em-jornadas-exaustivas)
- 🚫 **Condições precárias:** [Falta de estrutura nos postos de parada, higiene básica e outros.](https://www.ipea.gov.br/portal/categorias/45-todas-as-noticias/noticias/15073-estudo-revela-precarizacao-das-condicoes-de-trabalho-de-motoristas-e-entregadores-por-aplicativos)
- 🔐 **Insegurança:** [Roubo de cargas, violência nas estradas, medo constante.](https://ocarreteiro.com.br/roubo-de-carga/roubo-de-carga-2/)
- 👨‍👩‍👦 **Impacto pessoal:** Profissionais mais velhos permanecem por necessidade; jovens evitam entrar na carreira.
- 🎓 **Escolaridade e aspirações:** A predominância de ensino médio completo entre os motoristas sugere que níveis mais altos de escolaridade tendem a afastar os profissionais da carreira, pois outros setores oferecem melhores condições e reconhecimento.

---

## 📌 Conclusão

A análise dos dados formais do CAGED mostra um cenário **preocupante**: a força de trabalho está **envelhecendo rapidamente**, a entrada de jovens **não acompanha a saída** de veteranos, e **fatores econômicos, sociais e estruturais** tornam a carreira cada vez menos atrativa.

A escassez de motoristas é um fenômeno que vai além da demografia: trata-se de um reflexo de desvalorização estrutural da profissão. A regressão da idade média reflete a ausência de renovação, não um simples envelhecimento. O problema é agravado pela perda de poder aquisitivo, condições adversas de trabalho e pela imagem pouco atrativa da carreira. É urgente articular políticas públicas voltadas à formação, valorização e apoio à categoria.


