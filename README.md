# Topic-Modeling
Topic modeling architectures on COVID-19 tweets.

<b>Steps:</b>
<ul>
<li>Tweet extraction from pymongo</li>
<li>Tweet cleaning</li>
<li>Run topic models</li>
</ul>

We experiment on different topic modeling architectures:

<ul>
<li>LDA</li>
<li>GSDMM</li>
<li>BTM</li>
<li>LDA2Vec</li>
<li>BERT</li>
<li>Twitter-LDA (Java implementation)</li>
<li>Twitter-LDA (Python implementation)</li>
</ul>

BTM, GSDMM performs quite well for short text corpus like tweets. We intend to experiment on other models and show topic-coherence from the ouptput. 

#### Right now, Twitter-LDA is the winner. I have implemented both JAVA and Python version of the algorithm. We are workng on the performance metrics for evaluating the quality of our topic.
