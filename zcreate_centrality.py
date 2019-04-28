
def createhtml(data):
    
    with open("./centrality.html",'w') as f:
        
        INSERT = data.to_json()
        
        print INSERT
        
        contents = '''
        <script src="https://cdnjs.cloudflare.com/ajax/libs/rough.js/3.0.0/rough-async.es5.js"></script>
        <canvas id="myCanvas"></canvas>

        <script>
        width = window.innerWidth
        height = window.innerHeight
        document.getElementById("myCanvas").width=width
        document.getElementById("myCanvas").height = height 
        var rough = new rough.canvas(document.getElementById("myCanvas"), width, height);
        rough.strokeWidth = 2;
        rough.fill = "rgba(255,0,0,0.2)";

        function draw(data){
            
            var keys = Object.keys(data)
            var dh = height / (keys.length+1)
            margin = width*.25
            var dw  = (width-margin)/(Object.values(data[keys[1]]).length + 1)    
            keys.forEach((d,i)=>{
                var x = 0        
                Object.values(data[d]).forEach((c,j)=>{            
                    var e = rough.circle(margin + dw*j, i*dh, dw*c);
                    e.roughness = 1.5;
                    e.hachureAngle = 60;
                    e.hachureGap = 1.5;
                    e.fill= "rgb(10,150,10)";
                    e.fillWeight= 3; // thicker lines for hachure
                })
            })
            
            
        }

        data =''' + INSERT + '''

        draw(data)

        setTimeout(function() {
          location.reload();
        }, 5000);
        </script>
        '''
        
        print contents
        f.write(contents)