# 📘 Análise da Escassez de Motoristas no Brasil

---

## 🧭 1. Introdução

A escassez de motoristas profissionais no Brasil representa um desafio crescente e multifacetado para o setor de transporte e logística. Dada a predominância do modal rodoviário na movimentação de cargas e pessoas no país, a atuação dessa categoria é essencial para o pleno funcionamento da economia nacional.

Este estudo tem como objetivo principal analisar, por meio dos dados abertos do CAGED (Cadastro Geral de Empregados e Desempregados), as principais tendências trabalhistas associadas aos motoristas formais do setor de transporte. Mais do que identificar tendências, buscamos oferecer evidências sólidas para decisões estratégicas: **Por que estamos perdendo motoristas? O que afasta os jovens dessa carreira? E o que pode ser feito – agora – para evitar um colapso anunciado?**

Todo o estudo foi conduzido com foco no CBO (Classificação Brasileira de Ocupações) específico:

* **7825-10 | Motoristas de Caminhão (rotas regionais e internacionais).**

---

## 📚 2. Metodologia e Origem dos Dados

Este estudo apresenta uma análise aprofundada da dinâmica do mercado de trabalho para o CBO de **Motorista de Caminhão** no Brasil, utilizando uma base de dados robusta e proveniente de fontes oficiais. A análise principal foi desenvolvida com dados abertos do **CAGED (Cadastro Geral de Empregados e Desempregados)**, disponibilizados pelo Ministério do Trabalho e Emprego (MTE) via FTP, abrangendo o período de **2010 a 2024**.

Para garantir a consistência e completude da série histórica, os dados foram organizados da seguinte forma:

* **Dados de 2020 a 2024:** Extraídos do **Novo CAGED** via FTP.
    * `ftp://ftp.mtps.gov.br/pdet/microdados`
* **Dados de 2010 a 2019:** Obtidos do **CAGED Antigo** e, quando necessário, complementados por bases alternativas para correção de arquivos corrompidos.

Para contextualizar a remuneração, foram incorporados dados do **DIEESE (Departamento Intersindical de Estatística e Estudos Socioeconômicos)**, com foco na série histórica do **Salário Mínimo Necessário**, uma referência para o custo de vida digno de uma família brasileira de quatro pessoas.

Além disso, o estudo foi **expandido** para incluir informações do **Registro Nacional de Condutores Habilitados (RENACH/DENATRAN)**, acessível em:
* `https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-Senatran/estatisticas-quantidade-de-habilitados-denatran`

Com isso, foi possível estimar o **estoque de motoristas habilitados com categorias C, D e E**, com destaque para os ativos com menos de 70 anos, permitindo uma visão mais abrangente do potencial de mão de obra.

Informações complementares de *saldos* foram extraídas da **RAIS 2023**, também fornecida pelo MTE, para enriquecer a perspectiva sobre o impacto dos eventos históricos.

---

### 🔧 Métricas e Indicadores-Chave

Para avaliar a entrada, permanência e saída de profissionais no setor, foram utilizadas as seguintes métricas:

* **🔁 Taxa de Turnover**
    Mede o ritmo de trocas no setor, refletindo a volatilidade.
    $$ \text{Taxa de Turnover} = \frac{\text{Demissão}}{\left( \frac{\text{Admissão} + \text{Demissão}}{2} \right)} $$
    > *Quanto mais alta, maior a instabilidade – ou seja, o setor perde e ganha muitos profissionais com frequência.*

* **🔄 Rotatividade**
    Indica o peso das demissões no total de movimentações.
    $$ \text{Rotatividade} = \frac{\text{Demissão}}{(\text{Admissão} + \text{Demissão})} $$
    > *Alta rotatividade significa que poucas pessoas permanecem na profissão, o que pode indicar desinteresse ou condições desfavoráveis.*

* **📈 Atratividade**
    Representa o apelo da profissão para novos profissionais.
    $$ \text{Atratividade} = \frac{\text{Admissão}}{(\text{Admissão} + \text{Demissão})} $$
    > *Quanto maior, mais pessoas estão entrando no setor – um sinal de que a carreira ainda é vista como viável ou desejável.*

* **🔒 Retenção**
    Avalia a capacidade de manter quem é contratado.
    $$ \text{Retenção} = \frac{(\text{Admissão} - \text{Demissão})}{\text{Admissão}} $$
    > *Retenção alta significa que o setor consegue manter seus trabalhadores por mais tempo, reduzindo perdas.*

* **💸 Poder de Compra**
    Compara o salário dos motoristas com o salário mínimo, fornecendo uma visão da capacidade aquisitiva.
    $$ \text{Poder de Compra} = \frac{\text{Salário Médio}}{\text{Salário Mínimo}} $$
    > *Quanto maior, mais o trabalhador consegue comprar com seu salário. Queda nessa relação significa perda de poder aquisitivo.*

* **🚨 Escassez**
    Estima a dificuldade de reposição de profissionais, especialmente em cenários de perda líquida de vagas.
    $$ \text{Escassez} = \frac{|\text{Saldo Negativo}|}{\text{Admissão}} $$
    > *Se o saldo for negativo e proporcionalmente alto, indica que o setor está perdendo mais profissionais do que consegue repor – sinal claro de escassez.*

> ⚠️ **Nota Importante:** Os dados do CAGED podem passar por pequenas revisões com o tempo. Neste estudo, os valores foram arredondados para facilitar a leitura e focar nas **tendências e padrões**, sem prejuízo da confiabilidade geral da análise.

---

## 👥 3. Perfil Sociodemográfico dos Motoristas

### 3.1 Escolaridade

A análise da escolaridade dos motoristas de caminhão revela uma clara evolução no perfil educacional exigido pela profissão:

* **📘 Predominância do Ensino Médio Completo:** Desde 2011, essa faixa superou as demais, ultrapassando 70% em 2024. Em 2010, o grau mais comum era o **Ensino Fundamental Completo**, demonstrando uma **exigência crescente de escolaridade no setor**.
* **Implicações:** Essa mudança pode estar relacionada a:
    * Normas regulatórias mais rigorosas;
    * Adoção de tecnologias embarcadas nos veículos, que demandam maior conhecimento;
    * Redução do interesse de candidatos com maior escolaridade devido à percepção de baixa valorização da profissão.

| Ano  | Fundamental Completo | Fundamental Incompleto | Médio Completo | Médio Incompleto | Superior Completo | Superior Incompleto |
| :--- | :------------------- | :--------------------- | :------------- | :--------------- | :---------------- | :------------------ |
| 2010 | 44.83%               | 3.35%                  | 39.41%         | 11.69%           | 0.26%             | 0.44%               |
| 2011 | 41.02%               | 3.52%                  | 43.18%         | 11.54%           | 0.29%             | 0.44%               |
| 2012 | 38.05%               | 3.36%                  | 46.87%         | 10.95%           | 0.30%             | 0.47%               |
| 2013 | 35.73%               | 3.28%                  | 49.45%         | 10.67%           | 0.40%             | 0.48%               |
| 2014 | 33.72%               | 3.26%                  | 51.83%         | 10.28%           | 0.40%             | 0.51%               |
| 2015 | 32.14%               | 3.15%                  | 53.74%         | 9.96%            | 0.50%             | 0.51%               |
| 2016 | 31.21%               | 3.08%                  | 55.11%         | 9.65%            | 0.43%             | 0.52%               |
| 2017 | 30.31%               | 3.21%                  | 56.33%         | 9.19%            | 0.45%             | 0.52%               |
| 2018 | 30.06%               | 3.66%                  | 56.04%         | 9.16%            | 0.50%             | 0.58%               |
| 2019 | 28.43%               | 3.62%                  | 57.77%         | 8.99%            | 0.55%             | 0.60%               |
| 2020 | 25.00%               | 3.07%                  | 62.40%         | 8.18%            | 0.59%             | 0.59%               |
| 2021 | 22.66%               | 2.70%                  | 65.21%         | 7.97%            | 0.65%             | 0.61%               |
| 2022 | 21.03%               | 2.61%                  | 67.07%         | 7.66%            | 0.71%             | 0.71%               |
| 2023 | 19.65%               | 2.31%                  | 68.84%         | 7.44%            | 0.80%             | 0.73%               |
| 2024 | 18.69%               | 2.22%                  | 70.00%         | 7.29%            | 0.91%             | 0.68%               |

---

### 3.2 Gênero

A distribuição por gênero no setor de motoristas de caminhão formal continua a ser majoritariamente masculina, com poucas mudanças ao longo dos anos:

* **👨 Predomínio Masculino:** O sexo masculino representou consistentemente **mais de 98%** dos motoristas em toda a série histórica até 2024.
* **Crescimento Tímido da Participação Feminina:** Apesar de um crescimento modesto (de 0.73% em 2010 para 1.56% em 2024), o setor ainda carece de políticas públicas e privadas robustas para a **inclusão de mulheres** na condução de veículos pesados.
* **Barreiras para a Inclusão Feminina:** Fatores como o ambiente de trabalho historicamente hostil, desafios de segurança nas estradas e a ausência de infraestrutura básica adequada contribuem para a baixa entrada feminina na profissão.

| Ano  | Homens | Mulheres |
| :--- | :----- | :------- |
| 2010 | 99.27% | 0.73%    |
| 2011 | 99.21% | 0.79%    |
| 2012 | 99.17% | 0.83%    |
| 2013 | 99.14% | 0.86%    |
| 2014 | 99.01% | 0.99%    |
| 2015 | 99.02% | 0.98%    |
| 2016 | 99.04% | 0.96%    |
| 2017 | 99.07% | 0.93%    |
| 2018 | 99.16% | 0.84%    |
| 2019 | 99.10% | 0.90%    |
| 2020 | 98.97% | 1.03%    |
| 2021 | 98.82% | 1.18%    |
| 2022 | 98.66% | 1.34%    |
| 2023 | 98.57% | 1.43%    |
| 2024 | 98.44% | 1.56%    |

---

## 📈 4. Evolução e Diagnóstico da Categoria

### 4.1 🔹 Saldo de Vagas com Eventos Históricos

O gráfico de saldo de vagas por ano, contextualizado com eventos econômicos e sociais, oferece uma visão clara da sensibilidade do setor a fatores externos.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="1_saldo_eventos.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>2010–2013: Crescimento Moderado:</strong> Período de expansão econômica pós-crise global (2008/2009), refletindo um saldo positivo e consistente de vagas.</li>
            <li><strong>2014–2016: Saldo Negativo Impactante:</strong> Destaque para 2016, com um saldo de **–54.000 vagas**. Este período coincide diretamente com a Recessão Brasileira, caracterizada por queda acentuada do PIB, desemprego generalizado e retração do setor logístico.</li>
            <li><strong>2017–2021: Recuperação Lenta e Gradual:</strong> Sinais de estabilização e recuperação, com saldos voltando a ser positivos, embora em patamares mais modestos.</li>
            <li><strong>2022: Ano Atípico de Recuperação:</strong> Um ano de forte crescimento no saldo. Pode refletir a recuperação pós-COVID-19, um aumento da demanda logística impulsionada pelo e-commerce, e estímulos econômicos.</li>
            <li><strong>2023-2024: Retorno a Patamares Estáveis:</strong> O saldo volta a níveis mais consistentes, indicando uma fase de estabilização após as grandes flutuações.</li>
        </ul>
        <p>➡️ <i style="font-weight: bold; color: #FF0000;">Eventos Chave no Período:</i> Recessão Brasileira (2014-2016) | Greve dos Caminhoneiros (2018) | Pandemia (2020) | Guerra Rússia–Ucrânia (2022).</p>
    </div>
</div>

---

### 4.2 🔹 Admissões por Faixa Etária

A distribuição das admissões por faixa etária revela um dos maiores desafios para a renovação da categoria: o envelhecimento da base de entrada.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="2_distribuicao_admissao_faixa_etaria.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>📉 Queda Acentuada dos Jovens:</strong> A faixa etária de 18-24 anos, que representava aproximadamente 8% das admissões em 2010, cai para cerca de 4% em 2024. A faixa de 25-29 anos também recua significativamente, de aproximadamente 19% para 11%. Isso indica que <i>cada vez menos jovens estão ingressando na carreira de motorista de caminhão formal</i>.</li>
            <li><strong>⬆️ Aumento da Idade Intermediária:</strong> Em contraste, a faixa de 30-39 anos, embora com uma leve redução percentual geral, atingiu um pico de ~40% em 2016. As faixas de 40-49 e 50-64 anos mostram crescimento contínuo, subindo de ~24% e ~12% para ~32% e ~18% respectivamente.
            Ou seja, a base de entrada para a profissão está se tornando progressivamente mais velha.</li>
        </ul>
        <p>🚨 <i style="font-weight: bold; color: #FF0000;">Sinal de Escassez Futura:</i> Com poucos recém-entrantes e uma base de novos profissionais cada vez mais madura, o setor tende a envelhecer rapidamente e, a médio e longo prazo, enfrentar uma severa falta de força de trabalho qualificada e apta para as demandas físicas da profissão.</p>
    </div>
</div>

---

### 4.3 🔹 Idade Média dos Motoristas

Complementando a análise anterior, a evolução da idade média dos motoristas de caminhão formal confirma a tendência de envelhecimento da categoria.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="3_evolucao_idade_media.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>⬆️ Tendência Clara de Envelhecimento:</strong> A idade média dos motoristas sobe de 37,02 (aproximadamente 37 anos e 2 meses) anos em 2010 para 40,80 (aproximadamente 40 anos e 10 meses) anos em 2024. Um crescimento de quase 4 anos em um intervalo de 15 anos é expressivo, especialmente para uma profissão que exige vigor físico.</li>
            <li><strong>Pico de Crescimento entre 2014–2018:</strong> O aumento percentual mais acentuado (até +2,20%) ocorre neste período, que coincide com a queda de jovens nas admissões, reforçando a conexão entre a falta de renovação e o envelhecimento geral da categoria.</li>
            <li><strong>Estabilização Recente com Leve Flutuação:</strong> Pequenas variações entre 2020 e 2024 (+/- 0,05%) podem sugerir uma saturação ou limitação na entrada/saída de profissionais, refletindo um envelhecimento do estoque ativo com baixa renovação.</li>
        </ul>
        <p>➡️ <i style="font-weight: bold; color: #FF0000;">Conclusão:</i> Menos jovens estão entrando na profissão, aqueles que entram já são mais velhos e experientes, e a força de trabalho atual está envelhecendo sem uma substituição à altura, gerando um desequilíbrio geracional.</p>
    </div>
</div>

---

## 5. Análise Econômica e Indicadores de Dinâmica de Mercado

Esta seção explora como fatores econômicos e as dinâmicas internas do mercado de trabalho impactam a categoria de motoristas de caminhão.

### 5.1 🔸 Saldo de Empregos e Taxa de Turnover

A relação entre o saldo de empregos e a taxa de turnover é crucial para entender a saúde do mercado de trabalho para motoristas.


<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="5_empregados_turnover.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>Até 2014 - Volatilidade de Base e Estabilidade Relativa:</strong> O setor apresentava uma taxa de turnover em torno de 0.96. Este valor indica que para cada 100 contratações, aproximadamente 96 desligamentos ocorriam, refletindo um nível de volatilidade constante. Contudo, <strong>em comparação com os picos de rotatividade observados nos anos posteriores</strong>, este período demonstrou uma relativa estabilidade do emprego para os motoristas.</li>
            <li><strong>2014-2016 - Impacto da Recessão:</strong> Durante a recessão econômica, o turnover aumentou significativamente, refletindo um período de alta demissão e redução drástica no saldo total de empregos.</li>
            <li><strong>2017 - Recuperação Tímida, Turnover Elevado:</strong> Uma leve recuperação no saldo de empregos, mas o turnover permaneceu alto, sugerindo que a melhora não foi suficiente para gerar segurança no setor. Essa combinação de insatisfação pode ter contribuído para a greve dos caminhoneiros em 2018.</li>
            <li><strong>Pós-Greve (2019) e Pandemia (2020) - Recuperação da Demanda:</strong> Houve uma forte recuperação do saldo de empregos, impulsionada pela alta demanda por transporte, especialmente durante a pandemia. O turnover reduziu um pouco, refletindo uma melhor segurança e atratividade temporária.</li>
            <li><strong>2022 - Guerra na Ucrânia e Instabilidade:</strong> O saldo foi novamente impulsionado, mas o turnover voltou a crescer, indicando que, embora houvesse mais empregos, a instabilidade ou insatisfação dos motoristas persistia (possivelmente devido à pressão dos custos operacionais e incertezas econômicas globais).</li>
            <li><strong>2023 e 2024 - Estabilização Recente:</strong> Retorno do saldo a níveis mais baixos e do turnover a patamares semelhantes ao início da série histórica (2010-2011), refletindo uma retomada da estabilidade após períodos mais turbulentos.</li>
        </ul>
        <p>➡️ <i i style="font-weight: bold; color: #FF0000;">Conclusão:</i> O setor de transporte de carga é altamente sensível a choques econômicos e geopolíticos, com esses eventos impactando diretamente a rotatividade e a estabilidade dos empregos.</p>
    </div>
</div>

---

### 5.1.1 🔸 Saldo Acumulado e Taxa de Turnover

A visão acumulada do saldo de movimentações em conjunto com a taxa de turnover mostra o efeito de longo prazo das dinâmicas do mercado.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="5_empregados_acumulados_turnover.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
</div>
<div style="width: 100%; max-width: 900px; text-align: left;">
    <ul>
        <li><strong>Crescimento Acumulado até 2014:</strong> O saldo acumulado de movimentações cresceu consistentemente, indicando uma expansão líquida de empregos formais na categoria. Durante este período, a taxa de turnover se manteve em um **patamar de volatilidade de base**, que, embora não seja ideal para a estabilidade, representava o menor nível observado na série histórica até então.</li>
        <li><strong>Impacto da Recessão (2014-2016):</strong> O saldo acumulado sofre uma queda expressiva, e a taxa de turnover atinge seu pico histórico, evidenciando a intensidade da perda de empregos e a alta rotatividade no período.</li>
        <li><strong>Recuperação e Crescimento (2017-2024):</strong> Apesar dos desafios (greve, pandemia, guerra), o saldo acumulado retoma o crescimento, atingindo patamares significativos em 2024. No entanto, o turnover, embora não atinja os picos de 2016, mostra que a movimentação de entrada e saída de profissionais continua presente, indicando que a estabilidade ainda é um desafio.</li>
    </ul>
    <p>🔴 <i style="font-weight: bold; color: #FF0000;">Rotatividade Persistente:</i> Mesmo com saldos positivos e um crescimento acumulado, a rotatividade no setor ainda é elevada, o que sugere que, apesar das novas admissões, há uma dificuldade em reter os profissionais, resultando em uma instabilidade de mão de obra.</p>
</div>

---

### 5.2 🔸 Estoque de CNHs vs. Poder de Compra

A comparação entre o estoque de motoristas habilitados e seu poder de compra revela um descompasso preocupante entre a oferta potencial de mão de obra e a qualidade de vida.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="5_evolucao_estoque_poder_compra.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>2011-2015 - Expansão do Estoque, Queda do Poder de Compra:</strong> Período de crescimento consistente no número de motoristas habilitados, atingindo um pico de 13.16 milhões. No entanto, o poder de compra já apresentava sinais de deterioração, caindo de quase 2x o salário mínimo para patamares inferiores.</li>
            <li><strong>2016-2020 - Inversão de Tendência:</strong> Há uma queda no estoque de CNHs e uma continuidade na queda do poder de compra. Esse movimento pode indicar uma desmotivação da categoria diante da perda de capacidade de consumo e condições de trabalho menos atrativas, levando a uma não renovação ou abandono da profissão.</li>
            <li><strong>2021-2024 - Estabilização do Estoque, Poder de Compra em Baixa:</strong> O estoque de CNHs se estabiliza em um patamar mais baixo do que o pico de 2015, e o poder de compra continua estagnado ou em leve declínio.</li>
        </ul>
        <p>➡️ <i style="font-weight: bold; color: #FF0000;">Conclusão:</i> A perda de poder de compra, um reflexo da baixa remuneração em relação aos custos de vida, impacta diretamente a atratividade da profissão, desincentivando a renovação do estoque de motoristas habilitados. Muitos habilitados podem estar optando por outras atividades que ofereçam melhor retorno financeiro.</p>
    </div>
</div>

---

### 5.3 🔹 Salário Médio vs. Salário Mínimo vs. Mínimo Necessário (DIEESE)

A análise comparativa entre o salário médio dos caminhoneiros, o salário mínimo e o salário mínimo necessário calculado pelo DIEESE é um dos indicadores mais críticos para entender a atratividade da profissão.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="7_salario_medio_minimo_necessario.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>Salário Médio (Caminhoneiros):</strong> Cresce de aproximadamente R$ 975 em 2010 para cerca de R$ 2.500 em 2024. Embora tenha dobrado em termos nominais, este aumento não acompanhou o custo de vida real.</li>
            <li><strong>Salário Mínimo:</strong> Demonstra uma evolução lenta e linear, passando de R$ 510 para R$ 1.412 no mesmo período.</li>
            <li><strong>Mínimo Necessário (DIEESE):</strong> Este indicador, que representa o valor que uma família de 4 pessoas realmente precisaria para viver com dignidade no Brasil, sobe drasticamente de aproximadamente R$ 2.100 para mais de R$ 7.300.</li>
        </ul>
        <p>🚨 <i style="font-weight: bold; color: #FF0000;">Déficit de Renda:</i> O salário médio dos caminhoneiros formalizados sempre permaneceu bem abaixo do mínimo necessário para uma vida digna. Em 2024, ele cobria menos de 35% do valor considerado essencial. Esta disparidade justifica a baixa atratividade da profissão, pois o retorno financeiro não compensa o esforço, a jornada exaustiva e o desgaste físico, levando à fuga de jovens e ao envelhecimento da força de trabalho (Capítulo 9).</p>
    </div>
</div>

---

## 6. Indicadores e Estoque de Habilitações

Esta seção explora o panorama do estoque de motoristas habilitados no Brasil, crucial para entender a disponibilidade de mão de obra.

### 6.1 🔹 Evolução de CNHs Habilitadas para Conduzir Caminhão

A análise do estoque de CNHs aptas para dirigir caminhões (categorias C, D ou E) revela tendências importantes sobre a oferta potencial de motoristas.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="8_estoque_cnh.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>Crescimento Inicial e Pico:</strong> O total de CNHs aptas a dirigir caminhões cresceu de 11,8 milhões em 2011 para um pico de 13,2 milhões em 2015, indicando uma expansão na base de motoristas habilitados.</li>
            <li><strong>Queda Contínua (2016-2021):</strong> A partir de 2016, houve uma queda contínua no estoque, atingindo um mínimo de 11,41 milhões em 2021. Este declínio pode ser um reflexo da menor renovação de habilitações ou da inatividade de motoristas.</li>
            <li><strong>Leve Recuperação Recente:</strong> Desde 2022, observa-se uma leve recuperação, chegando a 11,55 milhões em 2024.</li>
        </ul>
        <p>➡️ <i style="font-weight: bold; color: #FF0000;">Implicação:</i> Este padrão indica um envelhecimento natural da frota habilitada, com renovação insuficiente para manter o crescimento observado no período pré-2016. Muitos motoristas podem estar deixando de renovar suas habilitações devido à falta de atratividade da profissão.</p>
    </div>
</div>

---

### 6.2 🔹 Estoque de CNH e Aumento da Faixa Etária (70+)

A combinação da queda no estoque total de CNHs com o aumento da parcela de habilitados com mais de 70 anos reforça o problema do envelhecimento da categoria.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="8_estoque_cnh_mais_70_idade_media.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>Queda no Estoque e Envelhecimento Concomitante:</strong> O estoque total de CNHs inicia um forte declínio (de 13,16 milhões para 11,41 milhões em 2021). Em paralelo, a parcela de habilitados com <strong>70 anos ou mais</strong> cresce significativamente, de 0,40 milhão (2011) para 1,18 milhão (2024). Isso sugere que a perda líquida de CNHs vem principalmente de desistências ou não-renovações entre motoristas mais jovens, enquanto a população mais idosa permanece ativa.</li>
            <li><strong>Aumento da Idade Média:</strong> A idade média dos motoristas habilitados acompanha esse deslocamento, saltando de aproximadamente 37 anos em 2011 para cerca de 40.8 (40 anos e 10 meses) anos em 2024. O aumento mais acentuado ocorre logo após o período de 2014–2016, reforçando que, mesmo com menos habilitados no total, o perfil que permanece é progressivamente mais velho.</li>
        </ul>
        <p>🚨 <i style="font-weight: bold; color: #FF0000;">Risco Duplo:</i> Essa combinação – estoque geral em queda e envelhecimento concentrado – aponta para um risco duplo para o setor: menos renovação de motoristas habilitados e aumento da vulnerabilidade a fatores de saúde e aposentadoria para a base de mão de obra ativa.</p>
    </div>
</div>

---

### 6.3 🔹 Estoque de CNHs vs. Motoristas Empregados Formalmente

Esta comparação crucial revela a lacuna entre o potencial de mão de obra e a efetiva utilização de motoristas no mercado formal.

<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 40px;">
    <img src="9_.png" style="width: 100%; max-width: 900px; height: auto; object-fit: contain; margin-bottom: 20px;">
    <div style="width: 100%; max-width: 900px; text-align: left;">
        <ul>
            <li><strong>Dados da RAIS 2023:</strong> Registrou 1.714.780 motoristas de caminhão formalmente empregados.</li>
            <li><strong>Estoque Total de Habilitados:</strong> O número de motoristas com habilitação (C, D ou E) para conduzir caminhões é de 11.550.608.</li>
            <li><strong>Grande Saldo Não Utilizado:</strong> Apenas aproximadamente 15% das pessoas que possuem habilitação para conduzir caminhão estão, de fato, atuando no setor formal.</li>
        </ul>
        <p>➡️ <i style="font-weight: bold; color: #FF0000;">Consideração Crucial:</i> Há um vasto reservatório de mão de obra potencialmente qualificada que não está sendo utilizada pelo setor formal. Isso sugere que a escassez de motoristas não é meramente uma falta de pessoas habilitadas, mas sim uma questão multifacetada, fortemente influenciada pela atratividade e pelas condições da profissão, que desmotivam muitos habilitados a ingressarem ou permanecerem no mercado formal de caminhões.</p>
    </div>
</div>

---

## 7. 🔍 Limitações do Estudo

É fundamental reconhecer as limitações deste estudo para uma interpretação precisa dos resultados:

* **Foco em Dados Formais (CAGED):** O CAGED não capta motoristas autônomos, Microempreendedores Individuais (MEIs) ou profissionais terceirizados via frota agregada. Isso significa que uma parcela significativa da força de trabalho, especialmente motoristas de aplicativos e caminhoneiros independentes, não está incluída na análise.
    > ⚠️ *Esses dados mostram apenas o contexto dos empregos **formais**, não necessariamente uma redução real na demanda desses profissionais no mercado total.*

* **Ausência de Dados Qualitativos Detalhados:** O estudo não pôde incluir informações detalhadas sobre a jornada de trabalho real (além das horas registradas formalmente), o tempo médio em rodovias, as pausas realizadas ou as condições de saúde específicas dos motoristas.

---

## 8. 🚫 Fatores Qualitativos da Profissão

Além dos dados quantitativos, é essencial considerar os fatores qualitativos que impactam diretamente a atratividade e a retenção de motoristas de caminhão:

* **💰 Remuneração Instável e Insuficiente:** Salários variáveis e muitas vezes inadequados frente às exigências do trabalho e aos custos de vida.
    * *Referências:* [CNT e Governo criam programa para diminuir falta de caminhoneiros Brasil](https://estradao.estadao.com.br/caminhoes/cnt-e-governo-criam-programa-para-diminuir-falta-de-caminhoneiros-brasil/)
* **🕐 Jornada Exaustiva:** Longas horas de trabalho, muitas vezes sem infraestrutura de apoio adequada ou tempo suficiente para descanso.
    * *Referências:* [Operação Jornada Legal flagra motoristas em jornadas exaustivas](https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2023/novembro/operacao-jornada-legal-flagra-motoristas-em-jornadas-exhaustivas)
* **🚫 Condições Precatórias:** Falta de estrutura básica em postos de parada, condições de higiene inadequadas e ausência de ambientes seguros para descanso.
    * *Referências:* [Estudo revela precarização das condições de trabalho de motoristas e entregadores por aplicativos](https://www.ipea.gov.br/portal/categorias/45-todas-as-noticias/noticias/15073-estudo-revela-precarizacao-das-condicoes-de-trabalho-de-motoristas-e-entregadores-por-aplicativos)
* **🔐 Insegurança:** Altos índices de roubo de cargas e violência nas estradas geram um medo constante, impactando a saúde mental e física dos profissionais.
    * *Referências:* [Roubo de carga](https://ocarreteiro.com.br/roubo-de-carga/roubo-de-carga-2/), [Insegurança é o principal ponto negativo da profissão de caminhoneiro](https://www.cnt.org.br/agencia-cnt/inseguran%C3%A7a-e-o-principal-ponto-negativo-da-profissao-de-caminhoneiro)
* **👨‍👩‍👦 Impacto Pessoal e na Saúde Mental:** O isolamento social, a ausência do convívio familiar e a pressão por produtividade afetam negativamente a saúde mental dos motoristas, contribuindo para quadros de estresse, ansiedade e depressão.
    * *Referências:* [A importância da saúde mental para motoristas de caminhão](https://www.garbuio.com.br/a-importancia-da-saude-mental-para-motoristas-de-caminhao/)
* **🎓 Escolaridade e Aspirações:** Embora a escolaridade média esteja aumentando, a predominância de ensino médio completo entre os motoristas sugere que níveis mais altos de escolaridade tendem a afastar os profissionais da carreira, pois outros setores podem oferecer melhores condições e reconhecimento, levando a uma busca por melhores oportunidades.
    * *Referências:* [Baixo rendimento e escolaridade prevalecem entre caminhoneiros brasileiros](https://monitormercantil.com.br/baixo-rendimento-e-escolaridade-prevalecem-entre-caminhoneiros-brasileiros)

---

## 9. 📌 Conclusão e Recomendações

A análise aprofundada dos dados do **CAGED**, RENACH e DIEESE revela um alerta claro: a categoria de motoristas de caminhão no Brasil enfrenta um processo acelerado de envelhecimento, com entrada insuficiente de novos profissionais para repor os que deixam a atividade. Se mantida essa tendência, o setor poderá enfrentar um colapso funcional nos próximos anos, com graves impactos para a economia do país.

Há um **grande reservatório de mão de obra potencialmente qualificada** (os mais de 11 milhões de habilitados C, D, E) que não está sendo utilizada pelo setor formal. Isso demonstra que a escassez não é apenas demográfica ou de formação inicial, mas uma questão estrutural, econômica e operacional, influenciada decisivamente pela **baixa atratividade da profissão**.

Entre os fatores identificados, a **perda de poder de compra** (salários muito abaixo do mínimo necessário para uma vida digna) e as **condições precárias de trabalho** (jornadas exaustivas, insegurança, falta de infraestrutura e impacto na saúde mental) se destacam como os principais entraves à atração e retenção de mão de obra.

Diante desse cenário, é urgente que lideranças públicas e privadas articulem estratégias coordenadas e eficazes para enfrentar o problema. Algumas diretrizes prioritárias incluem:

* **Revisão da Política de Remuneração:** Foco na recomposição do poder de compra dos salários, garantindo um retorno financeiro que justifique o investimento e o esforço exigido pela profissão.
* **Incentivos à Formação e Certificação Profissional:** Programas direcionados a jovens e mulheres, desmistificando a profissão e oferecendo capacitação de qualidade para ingresso no setor.
* **Investimentos em Infraestrutura e Segurança Rodoviária:** Melhoria das condições de descanso, segurança em postos de parada e combate eficaz ao roubo de cargas e à violência nas estradas.
* **Campanhas de Valorização da Profissão:** Iniciativas que resgatem a imagem e o prestígio da carreira de motorista de caminhão, focando na renovação geracional e mostrando as possibilidades de desenvolvimento.
* **Melhora das Condições de Trabalho e Bem-Estar:** Atenção à saúde mental dos motoristas, oferecendo suporte psicológico e promovendo um ambiente de trabalho mais humano e justo.

Sem ações concretas e coordenadas, a continuidade e a eficiência do transporte rodoviário – vital para a economia brasileira – estarão seriamente comprometidas.

---
*Estudo realizado em 29 de maio de 2025.*
