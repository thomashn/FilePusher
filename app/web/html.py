def makeHTMLFileTable(entryList):
    html = ("<table class='filetable'>")
    for entry in entryList:
        dlInfo = "("+str(entry.maxDownloads)+"/"+str(entry.timesDownloaded)+")"
        link = "<a href=download?fileURL="+entry.URL+">LINK</a>"
        html += ("<tr><td>"+entry.name+"</td><td>"+dlInfo+"</td>"
            "<td>"+link+"</td>"
            "<td><a href=delete?fileURL="+entry.URL+">DELETE</a></td></tr>")
            #"<td><a href='mailto:?subject=WHAT&body="+link+"'>MAIL</a></td></tr>")
    html += ("</table>")
    return html

def makeMailLink(url,domain,port,subject=None,body=None):
    html ="<a href='mailto:?subject="
    html += subject
    html += "&body="
    html += body
    html += ">Email</a>"
