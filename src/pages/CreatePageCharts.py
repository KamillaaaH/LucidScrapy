# -*- coding: utf-8 *-*
__author__="kamilla"
__date__ ="$Dec 8, 2012 1:34:34 PM$"

def createFile(fileName):
    file = open(fileName, 'w+')
    writeDoctype(file)
    writeHead(file, "MY TITLE")
    writeBody(file)
    

def writeDoctype(file):
    file.write('''<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"> \
    \n <html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\">''')


def writeHead(file, title):
    file.write('''<head> \
                \n <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8"/>
                <title>%s</title> \n
                <!-- CSS Files --> \n
                <link type=\"text/css\" href=\"css/base.css\" rel=\"stylesheet" /> \n
                <link type=\"text/css\" href=\"css/Treemap.css\" rel=\"stylesheet" /> \n
                <!--[if IE]><script language=\"javascript\" type=\"text/javascript\" src=\"../../Extras/excanvas.js"></script><![endif]--> \n
                <!-- JIT Library File --> \n
                <script language=\"javascript\" type=\"text/javascript\" src=\"js/jit.js"></script> \n
                <!-- Example File --> \n
                <script language=\"javascript\" type=\"text/javascript\" src=\"example2.js"></script> \n
                </head>''' %(title))

def writeBody(file):
    file.write('''<body onload="init();">
                  <div id="container">
                  <div id="left-container">
                  <div class="text">
                <h4>
                TreeMap with on-demand nodes
                </h4>

                This example shows how you can use the <b>request</b> controller method to create a TreeMap with on demand nodes<br /><br />
                This example makes use of native Canvas text and shadows, but can be easily adapted to use HTML like the other examples.<br /><br />
                There should be only one level shown at a time.<br /><br />
                Clicking on a band should show a new TreeMap with its most listened albums.<br /><br />

                </div>

                <div id="id-list">
                <table>
                    <tr>
                        <td>
                            <label for="r-sq">Squarified </label>
                        </td>
                        <td>
                            <input type="radio" id="r-sq" name="layout" checked="checked" value="left" />
                        </td>
                    </tr>
                    <tr>
                         <td>
                            <label for="r-st">Strip </label>
                         </td>
                         <td>
                            <input type="radio" id="r-st" name="layout" value="top" />
                         </td>
                    <tr>
                         <td>
                            <label for="r-sd">SliceAndDice </label>
                          </td>
                          <td>
                            <input type="radio" id="r-sd" name="layout" value="bottom" />
                          </td>
                    </tr>
                </table>
                </div>

                <a id="back" href="#" class="theme button white">Go to Parent</a>


                <div style="text-align:center;"><a href="example2.js">See the Example Code</a></div>
                </div>

                <div id="center-container">
                    <div id="infovis"></div>
                </div>

                <div id="right-container">

                <div id="inner-details"></div>

                </div>

            <div id="log"></div>
        </div>
    </body>
</html>''')


def main():
    createFile("test.html")


if __name__ == "__main__":
    main()




    