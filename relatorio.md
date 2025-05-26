<h1 align='center'> 📘 Análise da Escassez de Motoristas no Brasil</h1>

### 🧭 Introdução

  <p>  A escassez de motoristas profissionais no Brasil representa um desafio crescente para o setor de transporte e logística. A predominância do transporte rodoviário na movimentação de cargas e pessoas no país torna essa categoria essencial para o funcionamento da
  economia.</p>

 <p>
Este estudo visa analisar, por meio dos dados abertos do CAGED (Cadastro Geral de Empregados e Desempregados), 
as principais tendências trabalhistas associadas aos motoristas	formais do setor de transporte com foco no CBO 7825-10 	( Motoristas de Caminhão).
 </p>

---

###  Metodologia e Origem dos Dados
Este Estudo apresenta uma análise aprofundada da dinâmica do mercado de trabalho para o CBO de **Motorista de Caminhão** no Brasil, utilizando uma base de dados robusta e de fontes oficiais. A análise principal é fundamentada em dados abertos do **CAGED (Cadastro Geral de Empregados e Desempregados)**, fornecidos pelo Ministério do Trabalho e Emprego (MTE) via FTP, abrangendo o período de 2010 a 2024.
Para garantir a abrangência e a consistência histórica, os dados foram compilados da seguinte forma:
* Informações de **2020 até 2024** foram obtidas via FTP do **Novo CAGED** (ftp://ftp.mtps.gov.br/pdet/microdados).
* Dados de **2010 a 2019** foram extraídos majoritariamente via FTP do **CAGED Antigo**; para garantir a completude da série histórica, dados corrompidos foram complementados com uma base alternativa.

Para contextualizar a remuneração e sua adequação, o estudo incorporou dados do **DIEESE (Departamento Intersindical de Estatística e Estudos Socioeconômicos)**, uma instituição reconhecida por sua confiabilidade em análises socioeconômicas. Em particular, a série histórica do **Salário Mínimo Necessário** para uma família de quatro pessoas, calculada pelo DIEESE, foi utilizada para avaliar o poder de compra real dos salários na categoria de motoristas de caminhão.

As principais métricas utilizadas e suas respectivas formulações são:

* **Taxa de Turnover:** Calculada como a proporção entre o número de demissões e a média entre o número de admissões e demissões no período, ou seja, $\text{Demissão} / ((\text{Admissão} + \text{Demissão}) / 2)$. Esta métrica reflete a intensidade da rotatividade na força de trabalho.

* **Rotatividade:** Definida como a proporção das demissões em relação ao total de movimentações (soma de admissões e demissões), ou seja, $\text{Demissão} / (\text{Admissão} + \text{Demissão})$.

* **Atratividade:** Medida pela proporção das admissões em relação ao total de movimentações, ou seja, $\text{Admissão} / (\text{Admissão} + \text{Demissão})$. Esta métrica busca indicar o quão atraente o cargo é para novos talentos, em comparação com o volume de saídas.

* **Retenção:** Calculada como a proporção do saldo líquido de contratações em relação às admissões, ou seja, $(\text{Admissão} - \text{Demissão}) / \text{Admissão}$. Esta métrica reflete a eficiência da empresa em reter ou compensar as saídas com novas entradas.

* **Poder de Compra:** Representa a vantagem salarial relativa, sendo o quociente entre o salário médio do CBO e o salário mínimo oficial, ou seja, $\text{Salário Médio} / \text{Salário Mínimo}$.

* **Escassez:** Uma métrica calculada para indicar a dificuldade de reposição, representando a proporção do saldo negativo de vagas em relação às admissões, ou seja, $\text{np.round(np.where(saldo < 0, np.abs(saldo) / admissao, 0), 2)}$. Um valor maior indica maior dificuldade em preencher as vagas perdidas.

> `É importante ressaltar que, devido à natureza dos dados extraídos do CAGED, que podem apresentar pequenas revisões e variações ao longo do tempo, os valores numéricos apresentados e visualizados no relatório foram arredondados para facilitar a leitura e o entendimento das tendências gerais, sem prejuízo à fidedignidade da análise.`

---


<h2 align='center'> 👥 Perfil Sociodemográfico </h2>

### Escolaridade

- 📘  **Predominância do Ensino Médio Completo** desde 2011, ultrapassando 70% em 2024.
 Em 2010, o grau mais comum era o **Ensino Fundamental Completo**, mostrando uma **exigência crescente de escolaridade no setor**.
- Isso pode estar relacionado a:
  - Normas regulatórias mais rigorosas;
  - Adoção de tecnologias embarcadas;
  - Redução do interesse de candidatos com maior escolaridade por conta da baixa valorização da profissão.

| Ano  | Fundamental Completo | Fundamental Incompleto | Médio Completo | Médio Incompleto | Superior Completo | Superior Incompleto |
|------|----------------------|------------------------|-----------------|------------------|-------------------|---------------------|
| 2010 | 44.83%               | 3.35%                  | 39.41%          | 11.69%           | 0.26%             | 0.44%               |
| 2011 | 41.02%               | 3.52%                  | 43.18%          | 11.54%           | 0.29%             | 0.44%               |
| 2012 | 38.05%               | 3.36%                  | 46.87%          | 10.95%           | 0.30%             | 0.47%               |
| 2013 | 35.73%               | 3.28%                  | 49.45%          | 10.67%           | 0.40%             | 0.48%               |
| 2014 | 33.72%               | 3.26%                  | 51.83%          | 10.28%           | 0.40%             | 0.51%               |
| 2015 | 32.14%               | 3.15%                  | 53.74%          | 9.96%            | 0.50%             | 0.51%               |
| 2016 | 31.21%               | 3.08%                  | 55.11%          | 9.65%            | 0.43%             | 0.52%               |
| 2017 | 30.31%               | 3.21%                  | 56.33%          | 9.19%            | 0.45%             | 0.52%               |
| 2018 | 30.06%               | 3.66%                  | 56.04%          | 9.16%            | 0.50%             | 0.58%               |
| 2019 | 28.43%               | 3.62%                  | 57.77%          | 8.99%            | 0.55%             | 0.60%               |
| 2020 | 25.00%               | 3.07%                  | 62.40%          | 8.18%            | 0.59%             | 0.59%               |
| 2021 | 22.66%               | 2.70%                  | 65.21%          | 7.97%            | 0.65%             | 0.61%               |
| 2022 | 21.03%               | 2.61%                  | 67.07%          | 7.66%            | 0.71%             | 0.71%               |
| 2023 | 19.65%               | 2.31%                  | 68.84%          | 7.44%            | 0.80%             | 0.73%               |
| 2024 | 18.69%               | 2.22%                  | 70.00%          | 7.29%            | 0.91%             | 0.68%               |
| 2025 | 17.99%               | 2.23%                  | 70.64%          | 7.29%            | 0.92%             | 0.69%               |


-----

### Gênero

- 👨 **Predomínio esmagador do sexo masculino** em toda a série histórica — **mais de 98% até 2024**.
- Apesar de um **crescimento tímido da participação feminina**, o setor ainda carece de políticas públicas e privadas de **inclusão de mulheres** na condução de veículos pesados.
- Fatores como **ambiente de trabalho hostil, segurança nas estradas e ausência de infraestrutura básica** contribuem para a baixa entrada feminina.



| Ano  | Homem  | Mulher |
|------|--------|--------|
| 2010 | 99.27% | 0.73%  |
| 2011 | 99.21% | 0.79%  |
| 2012 | 99.17% | 0.83%  |
| 2013 | 99.14% | 0.86%  |
| 2014 | 99.01% | 0.99%  |
| 2015 | 99.02% | 0.98%  |
| 2016 | 99.04% | 0.96%  |
| 2017 | 99.07% | 0.93%  |
| 2018 | 99.16% | 0.84%  |
| 2019 | 99.10% | 0.90%  |
| 2020 | 98.97% | 1.03%  |
| 2021 | 98.82% | 1.18%  |
| 2022 | 98.66% | 1.34%  |
| 2023 | 98.57% | 1.43%  |
| 2024 | 98.44% | 1.56%  |
| 2025 | 98.41% | 1.59%  |



--------------------------------------------------------------------------



<h2 align='center'> Evolução e Diagnóstico da Categoria <h2>

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <div style="max-width: 880px;">   
  <h4> 🔹 Saldo de empregos com eventos históricos</h4> 
    <ul>
      <li><strong>2010–2013: </strong> Crescimento moderado → contexto de expansão econômica pós-crise global (2008/2009).</li>
      <li><strong>2014–2016:</strong> Saldo negativo severo, principalmente em 2016 (–54.000). (`Coincide com a Recessão Brasileira — queda no PIB, desemprego generalizado, retração do setor logístico.`)</li>
      <li><strong>2017–2021:</strong> Recuperação lenta e gradual, com sinais de estabilização..</li>
      <li><strong>2022:</strong> Ano atípico; Pode refletir recuperação pós-COVID + aumento da demanda logística (E-Commerce) + estímulos econômicos.</li>
      <li><strong>2023-2024:</strong> Nova queda, sugerindo perda de fôlego.</li>
    </ul>
    <p> Eventos econômicos: Recessão (2014-2016)| Greve dos caminhoneiros (2018)| Pandemia (2020) | Guerra Rússia–Ucrânia (2022)</p>
  </div>
  <img src="1_saldo_eventos.png" style="width: 880px;">
</div>

 ----------------

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <img src="2_distribuicao_admissao_faixa_etaria.png" style="width: 800px; margin-right: 30px;">
  <div style="max-width: 880px;">
    <h4>🔹 Admissões por faixa etária</h4>
    <ul>
      <li><strong>Queda dos Jovens:</strong>A faixa 18-24 cai de ~8 % em 2010 para ~4 % em 2024. A faixa 25-29 também recua de ~19 % para ~11 %. Isso indica que menos jovens estão entrando na carreira. </li>
      <li><strong>Aumento idade intermediária:</strong>A faixa 30-39 sobe de ~38 % para ~33 % (pico ~40 % em 2016). As faixas 40-49 e 50-64 crescem de ~24 % e ~12 % para ~32 % e ~18 %, respectivamente.
Ou seja, a base de entrada está cada vez mais velha.</li>    
    </ul>
    <p>Sinal de Escassez:</strong>Com poucos recém-entrantes, o setor tende a envelhecer e, a médio prazo, enfrentar falta de força de trabalho qualificada.</p>
  </div>
</div>

-------------------------------------------------------------------------------------------------------------------------------

-----

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <div style="max-width: 880px;">   
  <h4> 🔹 Idade média dos motoristas</h4> 
    <ul>
      <li><strong>Tendência clara de envelhecimento: </strong> A idade média sobe de 37,02 anos (2010) para 40,80 anos (2024). Crescimento de quase 4 anos em um intervalo de 15 anos, o que é expressivo considerando uma profissão operacional.</li>
      <li><strong>Aumento mais forte entre 2014–2018:</strong> Crescimento percentual mais acentuado (até +2,20%). Corresponde ao mesmo período em que o gráfico anterior mostrou queda de jovens nas admissões</li>
      <li><strong>Estabilização recente com flutuação leve: </strong> Pequenas variações entre 2020 e 2024 (+/- 0,05%), sugerindo saturação ou limitação de entrada/saída. Pode refletir envelhecimento do estoque ativo com baixa renovação.</li>     
    </ul>
    <p> Menos jovens estão entrando, os que estão, já entram mais velhos e a força de trabalho atual está envelhecendo, sem substituição à altura.</p>
  </div>
  <img src="3_evolucao_idade_media.png" style="width: 880px;">
</div>

-----

--------------------------------------------------------------------------------------------

<h2 align='center'> Indicadores de dinâmica de mercado<h2>


<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <div style="max-width: 880px;">   
  <h4> 🔸 Admissão vs Demissão + Turnover</h4> 
    <ul>
      <li><strong>2010–2013: </strong> Mercado aquecido, admissões superam demissões com folga.</li>
      <li><strong>2014–2017:</strong>  Inversão crítica — demissões passam admissões, gerando saldos negativos. </li>
      <li><strong>2018–2024: </strong> Retomada cíclica, com destaque para 2021–2024 (forte expansão).</li>
      <li><strong>Turnover 2016 (~1.08): </strong> Momento de mais instabilidade do setor.</li>
      <li><strong>Turnover até 2021 (~ 0.94): </strong> Sugere menor movimentação — pode indicar retenção forçada ou baixa atratividade.</li>         
    </ul>
    <p> Setor reage, mas não resolve: admissões voltam a subir, turnover ainda preocupa.</p>
  </div>
  <img src="5_admissoes_demissoes_turnover.png" style="width: 880px;">
</div>


-----------------------------

<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <img src="6_rotatividade_saldo.png" style="width: 800px; margin-right: 30px;">
  <div style="max-width: 880px;">
    <h4>🔸 Saldo vs Rotatividade </h4>
    <ul>
      <li><strong>2010-2013:</strong> Crescimento moderado, com saldos positivos.</li>
      <li><strong>2013-2017:</strong> Colapso total da contratação líquida — saldos negativos crescentes, com pico em 2016 (–54.000).</li>    
     <li><strong>2018-:</strong> Recuperação progressiva, com saldo positivo em todos os anos até 2024.</li>
    </ul>
    <p>🔴 Rotatividade:</strong>Alta rotatividade em 2015–2016 (~0.54) indica instabilidade severa, com muitos desligamentos, Queda consistente até 2021 (~0.47) pode sugerir menor movimentação por retração do mercado, ou, <br>
    etenção de profissionais mais velhos sem substituição (como indicado nos outros gráficos).</p>
    <p>Mesmo com saldos positivos, o setor ainda gira em círculos: a rotatividade segue elevada.</strong></p>
  </div>
</div>


----

<h2 align='center'> Análise Econômica: o Salário como Fator Estruturante <h2>


<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <div style="max-width: 880px;">   
  <h4> 🔹 Saldo vs Poder de Compra</h4> 
    <ul>
      <li><strong></li>
      <li><strong>2014–2017:</strong>  Tendência preocupante, saldo negativo até -54 mil. </li>
      <li><strong>2018–2024: </strong> Recuperação pós 2018, com perda de a partir de 2023.</li>
      <li><strong>Poder de Compra (salários mínimos): </strong> Pico em 2011 (~1.96) e queda contínua até 2024 (~1.74)</li>      
    </ul>
    <p> Mesmo com salário médio aumentando nominalmente, o mínimo cresceu mais → perda de poder de compra real. Fica evidente que ganhar mais em valor absoluto não significa manter o padrão de vida.</p>
  </div>
  <img src="7_saldo_poder_compra.png" style="width: 880px;">
</div>


-----------------------------


<div style="display: flex; align-items: flex-start; margin-bottom: 40px;">
  <img src="7_salario_medio_minimo_necessario.png" style="width: 800px; margin-right: 30px;">
  <div style="max-width: 880px;">
    <h4>🔹 Salário Médio vs Mínimo vs DIEESE </h4>
    <ul>
      <li><strong>🔵 Salário Médio (Caminhoneiros): </strong> Cresce de ~R$ 975 (2010) para ~R$ 2.500 (2024). Dobrou em termos nominais, mas não acompanhou o custo de vida real (linha laranja).</li>
      <li><strong>⚫ Salário Mínimo</strong> Evolução lenta e linear: R$ 510 → R$ 1.412.</li>    
     <li><strong>🟠 Mínimo Necessário (DIEESE)</strong> Sobe de ~R$ 2.100 para mais de R$ 7.300.Mostra quanto uma família de 4 pessoas realmente precisaria para viver com dignidade no Brasil.</li>
    </ul>  
    <p>Mais contratações, menos poder de compra: um setor pressionado?<br></p>
    <p>"Mesmo com aumento, o salário do caminhoneiro cobre menos de 35% do mínimo necessário para viver dignamente". O Salário médio dos caminhoneiros sempre ficou bem abaixo do mínimo necessário.<br>
    Isso justifica a baixa atratividade da profissão, Não compensa o esforço, jornada e desgaste físico e leva à fuga de jovens e envelhecimento da força de trabalho.</p>
  </div>
</div>

-------

-----

<h2 align='center'> 🔍 Limitações do Estudo <h2>


- **CAGED não capta autônomos nem MEIs**, o que deixa de fora uma parcela significativa da força de trabalho, especialmente:
  - Motoristas de aplicativos
  - Caminhoneiros independentes
  - Profissionais terceirizados via frota agregada

- **Ausência de dados sobre jornada de trabalho**, tempo médio em rodovias, pausas ou condições de saúde.


> ⚠️ Esses dados mostrados refletem apenas o contexto dos empregos **formais**, não necessariamente uma redução real na demanda desses profissionais.


-----

<h2 align='center'> 🚫 Fatores Qualitativos da Profissão <h2>

- 💰 **Remuneração instável:** [Salários variáveis e muitas vezes insuficientes frente às exigências do trabalho.](https://estradao.estadao.com.br/caminhoes/cnt-e-governo-criam-programa-para-diminuir-falta-de-caminhoneiros-brasil/)
- 🕐 **Jornada exaustiva:** [Longas horas de trabalho com pouco suporte na estrada.](https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2023/novembro/operacao-jornada-legal-flagra-motoristas-em-jornadas-exaustivas)
- 🚫 **Condições precárias:** [Falta de estrutura nos postos de parada, higiene básica e outros.](https://www.ipea.gov.br/portal/categorias/45-todas-as-noticias/noticias/15073-estudo-revela-precarizacao-das-condicoes-de-trabalho-de-motoristas-e-entregadores-por-aplicativos)
- 🔐 **Insegurança:** [Roubo de cargas, violência nas estradas, medo constante.](https://ocarreteiro.com.br/roubo-de-carga/roubo-de-carga-2/)
- 👨‍👩‍👦 **Impacto pessoal:** Profissionais mais velhos permanecem por necessidade; jovens evitam entrar na carreira.
- 🎓 **Escolaridade e aspirações:** A predominância de ensino médio completo entre os motoristas sugere que níveis mais altos de escolaridade tendem a afastar os profissionais da carreira, pois outros setores oferecem melhores condições e reconhecimento.

---------------

<h2 align='center'> Conclusão <h2>

A análise dos dados do CAGED revela um cenário preocupante para a categoria de motoristas de caminhão no Brasil. A força de trabalho está envelhecendo rapidamente, e a entrada de novos profissionais não tem sido suficiente para compensar a saída dos mais experientes. Esse desequilíbrio evidencia um risco real de colapso no setor nos próximos anos.

Embora múltiplos fatores contribuam para essa escassez, os dados apontam que a questão salarial é o principal obstáculo. A perda de poder de compra, somada às condições adversas de trabalho, tem afastado jovens da profissão e dificultado a permanência dos que já atuam na área.

Diante desse cenário, é fundamental a articulação de políticas públicas que promovam a formação profissional, incentivem a entrada de jovens, ampliem a participação de mulheres na categoria e melhorem as condições estruturais da atividade. Sem essas medidas, a tendência é de agravamento da crise de mão de obra no transporte rodoviário nos próximos anos.


