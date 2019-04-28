function merge_linktype(links){
    //combines multilinks of same reaction type
    // run before simulation
    var keep = []
    var parse = []
    
    links.forEach(i=>{
        comb = `${i.source}->${i.target}`
        if (!parse.includes(comb)){

            var q = {};
            links.forEach(j=>{
                
                if (j.source === i .source & j.target === i.target){
                    q[j.group] = q[j.group]||0
                    q[j.group] += 1
                }

           })
        Object.keys(q).forEach(g=>{
            i.group = g
            i.value = q[g]
            keep.push(i)
        })
        parse.push(comb)
   }})
    
    return keep
}

function merge_linkdir(links){
    //combines multilinks of same reaction type
    // run before simulation
    var keep = []
    var parse = []
    
    links.forEach(i=>{
        var lc = [i.source,i.target]
        lc.sort()
        
        comb = `${lc[0]}->${lc[1]}`
        
        if (!parse.includes(comb)){

            var q = 0;
            links.forEach(j=>{
                
                if ((j.source === i .source & j.target === i.target)|(j.target === i .source & j.source === i.target)){
                    q+=1
                }

           })
            i.value = q
            keep.push(i)
        
        parse.push(comb)
   }})
    
    return keep
}


        function rescale(){
            svg = d3.select('svg');
            var xmargin = ymargin= 50
            var x=[],y=[];
             [...document.querySelectorAll('circle')].forEach(i=>{
                 try{
                 var val = i.transform.baseVal[0].matrix

                 x.push(val.e)
                 y.push(val.f)
             }
             catch(err){
                 x.push(i.getAttribute('cx'))
                 y.push(i.getAttribute('cy'))
             }
             
             })
            svg.attr('viewBox',`${Math.min(...x)-xmargin/2} ${Math.min(...y)-ymargin/2} ${Math.max(...x)-Math.min(...x)+xmargin} ${Math.max(...y)-Math.min(...y)+ymargin}`)
            
        }
       
        //d3.selectAll('svg').each(rescale)


function fixpos(graph){
    graph.nodes = graph.nodes.map(e=>{e.fx=e.x; e.fy=e.y; return e})
    return graph
}

function savepos(graph){
    
    var json = JSON.stringify(fixpos(graph))
    var fs = require('fs');
fs.writeFile('savedpos.json', json, 'utf8');
console.log('saving')
    
}