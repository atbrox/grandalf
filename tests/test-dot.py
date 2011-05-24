#!/usr/bin/env python

import  pdb

from  grandalf.graphs  import *
from  grandalf.layouts import *

try:
  from  iod.syntax.text.dot.parser import parser
except ImportError:
  print "test-dot.py uses the dot parser of the 'iod' package."
  print "This parser (in 'iod/syntax/text/dot/parser.py') was not found." 
  print "checkout the iod git tree and retry."
  

mypdb  = pdb.Pdb()

L  = parser.parse(file('samples/dg10.dot').read())

G  = []

for  ast in L:
    print "testing graph %s :"%ast.name,
    V = {}
    E = []
    for k,x in ast.nodes.iteritems():
        try:
            v = Vertex(x.atr['label'])
        except (KeyError,AttributeError):
            v = Vertex(x.name)
        v.view = VertexViewer(10,10)
        V[x.name] = v
    print len(V)
    edgelist = []
    for e in ast.edges: edgelist.extend(e)
    for edot in edgelist:
        v1 = V[edot.n1.name]
        v2 = V[edot.n2.name]
        E.append(Edge(v1,v2))
    #mypdb.set_trace()
    G.append(Graph(V.values(),E))
    print "  [%d vertices]"%G[-1].order()
    print "  [%d groups]"%len(G[-1].C)
    for gr in G[-1].C:
    # Sugiyama algorithm applies only on directed acyclic graphs.
    # Of course if gr is undirected, it just means that setting a
    # default direction for an edge is meaningless and should not
    # change its mathematical properties...
    # The acyclic property is more difficult: If the graph has
    # some cycles, we need to invert some edges to remove any cycle
    # just for the Sugiyama drawing,
    # and the difficulty comes from selecting a set of
    # edges that need to be temporarily inverted.
    #
    # now we need to find "roots" vertices.
    # The following algorithm finds all vertex with
    # no incoming edge :
        r = filter(lambda x: len(x.e_in())==0, gr.sV)
    ## if len(r)==0, there exist at least one cycle in gr.
    ## finding a "good" set of roots depends now on inverting
    ## some edges. This can be done by redefining a graph_core
    ## with only 
        print "    . %d verts, %d root(s)"%(gr.order(),len(r))

        if len(r)==0:
            print 'no root found! default root is initial node.'
            r = [gr.sV.o[0]]

        print 'using tarjan algorithm to find inverted_edges...'
        L = gr.get_scs_with_feedback(r)

        sug = SugiyamaLayout(gr)

        sug.init_all(roots=r,inverted_edges=filter(lambda x:x.feedback, gr.sE))
        sug.draw()
        #for s in sug.draw_step(): pass
        for v,x in sug.grx.iteritems():
            label = v.data if hasattr(v,'data') else '*'
            print label, x, v.view.xy
        print 'Sugiyama drawing done.'.ljust(80,'_')
