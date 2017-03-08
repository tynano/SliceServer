# SliceServer
Simple SliceMatrix-IO Server in NodeJS and ZeroRPC

This project is a quick example of how to create a Web-App using the <a href = "http://www.slicematrix.io">SliceMatrix-IO</a> machine learning Platform as a Service (PaaS). The server delivers a single-page web app which displays a d3.js network graph based on the correlation between components of the S&P 500 stock index. 

A working example can be found at: www.slicematrix.io/finetwork
<a href="http://www.slicematrix.io/finetwork" target = "_blank"><img alt="Stock Market Network Graph powered by SliceMatrix-IO" src="assets/heat.png?raw=true" height='400px'></img></a>

Basic architecture includes:

<ul>
<li>D3 JS client to render the network</li>
<li>NodeJS Express server to relay user requests to the backend (via ZeroRPC)</li>
<li>Backend RPC server which uses <a href = "https://github.com/tynano/slicematrixIO-python">slicematrixIO-python</a> to dispatch requests to the IO Platform (Isomap)</li>
<li>Periodic training script (train.py) which downloads the price data from Yahoo finance and trains the initial network graph model</li>
</ul>
