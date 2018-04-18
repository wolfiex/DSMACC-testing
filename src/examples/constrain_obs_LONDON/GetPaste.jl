using Polynomials
using UnicodePlots
searchdir(path,key) = filter(x->contains(x,key), readdir(path))

csvfiles = searchdir("./",".csv")






function fitobs(species,x,y,order = 40)

    xaxis = 1:length(x)#linspace(0,1,length(x))
    println(xaxis)
    fit = polyfit(y,xaxis)
    print(fit)
    #Since this will be run in a terminal we can use unicode plotting to check that we are not overfitting.
    ypred = [fit(x) for x in xaxis] #divided by 1e-8 to get rid of the log axis requirement as per original plot

    println(ypred)
    #plotting
    #myplot = lineplot(xaxis,ypred, title = species, name = "Prediction",  color=:blue,border=:bold)
    #myplot = scatterplot!(myplot, xaxis,y, name = "Observations",color=:magenta)

    println(myplot)
end

x=[]
y=[]
for file in csvfiles

    names = split(file,"-pp")
    scale = names[2][1]
    if scale == 't' scale = 1e-12
    elseif scale == 'v' scale = 1e-9
    else scale = 1

    end
    data = []
    open(file) do f
       data = [split(i,",") for i in readlines(f)]
    end
    x = [float(i[1]) for i in data]
    y = [log10(float(i[2])*scale) for i in data]
    myplot = scatterplot(x,y, name = "Observations",color=:magenta)
    fitobs(names[1],x,y)

end
