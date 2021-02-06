## About

PageRank captures the importance of pages on the web. A page is important if it is pointed by many important pages. The Web can be represented with a Web graph matrix M = {mij}. Each page i corresponds to row i and column i of the matrix M. In this matrix M:

+ mij = 1/n j if page i is one of the n j children of page j;
+ mij = 0 otherwise.

The simple PageRank equation is p = M∗p where p is a vector of size N∗1 (where N is the number of nodes in the graph). p[i,1] represents the PageRank of page. The above multiplication of M with p is repeated until there is convergence to a solution. 

I implemented first a simple version of PageRank. I didn't create the matrix M directly because is too expensive. A row and a column would be needed for every id of the nodes and that would require 3,359361116736 Terabytes of RAM. M is actually very sparse (many cell are equal to 0) because a node is only child of a handful of other nodes and every node has relatively few children. Taking this into account M was built by reading the data of "web-Google.txt" by rows, with every child storing the position of the father (the column) and being placed in the jth row. It does not matter that those elements are in order because the PageRank involves multiplying a matrix by a vector where additions are involved that can be performed in any order yielding the same result. 

I then implemented an improved version of PageRank (p = α∗M∗p + (1−α)∗I), where α is a numeric value, N is the number of pages (nodes) in the Web graph, and I is a unary vector (i.e., all values are set to 1) of size N∗1. 

"pagerank.py" includes both algorithms and runs them with different parameters on the "web-Google.txt" data.

## How to execute

+ Install Python;
+ How to run 'pagerank.py':
	* open terminal;
	* navigate to the directory of 'pagerank.py';
	* type 'python pagerank.py' in the terminal to run.
+ Make sure 'web-Google.txt' is in the same directory as the executable. Download from "https://snap.stanford.edu/data/web-Google.html";
+ Python dependencies not part of standard library: matplotlib.
