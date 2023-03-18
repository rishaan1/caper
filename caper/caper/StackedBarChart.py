import pandas 
import plotly.express as px
# file = "/Users/TajanKenkreHomeMac1/Desktop/BafnaCode/aggregated_results.csv"
def StackedBarChart(file):
    df = pandas.read_csv(file, sep = ",", header = None)
    print(df.head())
    df.columns = ['Focal Amplification Classification' if x==4 else x for x in df.columns]
    df.columns = ['Sample' if x==1 else x for x in df.columns]
    df.columns = ['Amplicon Number' if x==2 else x for x in df.columns]
    df['Focal Amplification Classification'] = df['Focal Amplification Classification'].replace('Classification','No amp')
    df = df[~df.isin(['No amp']).any(axis=1)]
    fig = px.histogram(df, x = "Focal Amplification Classification")
    fig.update_layout(yaxis_title="Sample Count") 
    fig.show()
    df = df.filter(["Sample","Focal Amplification Classification"], axis=1)
    fig = px.bar(df, x="Sample", color="Focal Amplification Classification",
                barmode = 'stack')
    fig.show()
    df.drop(index=df.index[0], axis=0, inplace=True)
    df.head()
    df2 = df.groupby(['Sample','Focal Amplification Classification'])['Focal Amplification Classification'].count().reset_index(name='counts')
    df = pandas.DataFrame(df2)
    list1 = df2.values.tolist()
    for x in range(len(list1)):
        if list1[x][1] == "ecDNA":
            list1[x][1]  = "A" + list1[x][1]           
    df = pandas.DataFrame(list1, columns = ['Sample', 'Focal Amplification Classification','Count'])
    df = df.sort_values(["Focal Amplification Classification"], ascending = True)
    df = df.sort_values(["Count"], ascending = False)
    list1 = df.values.tolist()
    for x in range(len(list1)):
        if list1[x][1] == "AecDNA":
            list1[x][1]  = list1[x][1][1:]
    df = pandas.DataFrame(list1, columns = ['Sample', 'Focal Amplification Classification','Count'])
    output = df.pivot(index='Sample', columns='Focal Amplification Classification', values='Count')

    df = output.sort_values(['ecDNA', 'BFB', 'Complex non-cyclic', 'Linear amplification'], ascending=[False, False, False, False])
    df2 = df.reset_index()
    fig = px.bar(df2, x="Sample",y = ["ecDNA", "BFB", "Complex non-cyclic", "Linear amplification"], 
                barmode = 'stack',color_discrete_map = {
                        'ecDNA' : "rgb(255, 0, 0)",
                        'BFB' : 'rgb(0, 70, 46)',
                        'Complex non-cyclic' : 'rgb(255, 190, 0)',
                        'Linear amplification' : 'rgb(27, 111, 185)'}, hover_data = {'Sample':False})
    fig.update_layout(showlegend=False)
    fig.update_layout(yaxis_title="Number of focal amps")
    fig.show()
    return fig.to_html(full_html = False, div_id = "project_plotly_div")
