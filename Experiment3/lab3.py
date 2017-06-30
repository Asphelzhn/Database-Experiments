# -*- coding: utf-8 -*-
import sys
import locale
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import MySQLdb
reload(sys)

mycode = locale.getpreferredencoding()
code = QTextCodec.codecForName(mycode)
QTextCodec.setCodecForLocale(code)

conn = MySQLdb.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="1996210zhn",
    db="lab3",
    charset='utf8'
)
cur = conn.cursor()

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class StockDialog(QDialog):
    def __init__(self, parent=None):
        super(StockDialog, self).__init__(parent)
        self.setGeometry(300, 100, 300, 300)
        self.setWindowTitle('Lab3')
        palette1 = QPalette(self)
        palette1.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette1)
        mainSplitter = QSplitter(Qt.Vertical)
        mainSplitter.setOpaqueResize(True)

        listWidget = QListWidget(mainSplitter)
        listWidget.insertItem(0, self.tr("ER图"))
        listWidget.insertItem(1, self.tr("视图"))
        listWidget.insertItem(2, self.tr("插入"))
        listWidget.insertItem(3, self.tr("删除"))
        listWidget.insertItem(4, self.tr("查询"))

        frame = QFrame(mainSplitter)
        stack = QStackedWidget()
        stack.setFrameStyle(QFrame.Panel | QFrame.Raised)

        show_ER = showER()
        view = View()
        insert = Insert()
        delete = Delete()
        query = Query()
        stack.addWidget(show_ER)
        stack.addWidget(view)
        stack.addWidget(insert)
        stack.addWidget(delete)
        stack.addWidget(query)

        closePushButton = QPushButton(self.tr("退出"))

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(closePushButton)

        mainLayout = QVBoxLayout(frame)
        mainLayout.setMargin(6)
        mainLayout.setSpacing(6)
        mainLayout.addWidget(stack)
        mainLayout.addLayout(buttonLayout)

        self.connect(listWidget, SIGNAL("currentRowChanged(int)"), stack, SLOT("setCurrentIndex(int)"))
        self.connect(closePushButton, SIGNAL("clicked()"), self, SLOT("close()"))

        layout = QHBoxLayout(self)
        layout.addWidget(mainSplitter)
        self.setLayout(layout)


class showER(QWidget):
    def __init__(self, parent=None):
        super(showER, self).__init__(parent)
        pixmap = QPixmap("pic/ER.png")
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 0)

    def excute(self):
        print ("do not pressed the button to excute.")


class View(QWidget):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        labe11 = QLabel(self.tr("视图名："))
        label2 = QLabel(self.tr("表名："))
        label3 = QLabel(self.tr("视图属性："))
        label4 = QLabel(self.tr("限制："))
        button = QPushButton(self.tr("执行"))
        label5 = QLabel(self.tr("执行结果："))

        self.vnameEdit = QLineEdit()
        self.viewEdit = QLineEdit()
        self.attrEdit = QLineEdit()
        self.limitEdit = QLineEdit()
        self.resultEdit = QTextEdit()

        layout = QGridLayout(self)
        layout.addWidget(labe11, 0, 0)
        layout.addWidget(self.vnameEdit, 0, 1)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.viewEdit, 1, 1)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.attrEdit, 2, 1)
        layout.addWidget(label4, 3, 0)
        layout.addWidget(self.limitEdit, 3, 1)
        layout.addWidget(button, 4, 0)
        layout.addWidget(label5, 5, 0)
        layout.addWidget(self.resultEdit, 5, 1)


        self.connect(button, SIGNAL("clicked()"), self.excute)

    def excute(self):
        vname = self.vnameEdit.text()
        view = self.viewEdit.text()
        attr = self.attrEdit.text()
        query ="Create view "+ vname +" as "+ "select " + attr + " from " + view
        limit = self.limitEdit.text()
        if len(str(limit)) > 0:
            query += " where " + limit
        print query
        #        query = "select * from people"
        a2 = cur.execute(str(query))
        info = cur.fetchmany(a2)
        query2 ="select * from lab3." + vname
        print query2
        a3 = cur.execute(str(query2))
        info2 = cur.fetchmany(a3)
        result = ""
        temp = attr.split(',')
        for i in temp:
            result += "   "
            result += i
        result += '\n\n'
        for i in info2:
            for j in i:
                result += " "
                result += str(j)
            result += '\n'
        if len(result) > 0:
            #unicode(result.toUtf8(),'utf-8','ignore').encode('gbk')
            self.resultEdit.setText(result)
        else:
            self.resultEdit.setText("Cannot excute\"" + str(query) + "\"")


class Insert(QWidget):
    def __init__(self, parent=None):
        super(Insert, self).__init__(parent)

        label1 = QLabel(self.tr("表名："))
        label2 = QLabel(self.tr("值："))
        button = QPushButton(self.tr("执行"))
        label3 = QLabel(self.tr("执行结果："))

        self.tableEdit = QLineEdit()
        self.attrEdit = QLineEdit()
        self.resultEdit = QTextEdit()

        layout = QGridLayout(self)
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.tableEdit, 0, 1)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.attrEdit, 1, 1)
        layout.addWidget(button, 2, 0)
        layout.addWidget(label3, 3, 0)
        layout.addWidget(self.resultEdit, 3, 1)
        self.connect(button, SIGNAL("clicked()"), self.excute)

    def excute(self):
        table = self.tableEdit.text()
        value = self.attrEdit.text()
        query = "insert into " + str(table) + " values(" + str(value) + ")"
        print query

        try:
            a2 = cur.execute(query)
            info = cur.fetchmany(a2)
            result = ""
            for i in info:
                for j in i:
                    result += " "
                    result += j
                result += '\n'
            self.resultEdit.setText("Successed to insert the values into " + table)
        except MySQLdb.Warning,w:
            warning="Cannot insert ,because "+str(w)
            self.resultEdit.setText(unicode(warning,'utf-8','ignore'))
        except MySQLdb.Error,e:
            erro="Cannot insert ,becauese "+str(e)
            self.resultEdit.setText(unicode(erro,'utf-8','ignore'))



class Delete(QWidget):
    def __init__(self, parent=None):
        super(Delete, self).__init__(parent)

        label1 = QLabel(self.tr("表名："))
        #label2 = QLabel(self.tr("选择删除属性值："))
        label3 = QLabel(self.tr("限制："))
        button = QPushButton(self.tr("执行"))
        label4 = QLabel(self.tr("执行结果："))

        self.tableEdit = QLineEdit()
        #self.attrEdit = QLineEdit()
        self.limitEdit = QLineEdit()
        self.resultEdit = QTextEdit()

        layout = QGridLayout(self)
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.tableEdit, 0, 1)
        #layout.addWidget(label2, 1, 0)
        #layout.addWidget(self.attrEdit, 1, 1)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.limitEdit, 2, 1)
        layout.addWidget(button, 3, 0)
        layout.addWidget(label4, 4, 0)
        layout.addWidget(self.resultEdit, 4, 1)
        self.connect(button, SIGNAL("clicked()"), self.excute)

    def excute(self):
        table = self.tableEdit.text()
        #attr = self.attrEdit.text()
        query = "delete " + "from " + table
        limit = self.limitEdit.text()
        #print limit
        if len(limit) > 0:
            query += " where " + limit
        print query
        #        query = "select * from people"
        try:
            a2=cur.execute(str(query))
            info = cur.fetchmany(a2)
            print info
            self.resultEdit.setText("Successed to delete the values on " + table)
        except MySQLdb.Warning,w:
            warning="Cannot delete or update a parent row: "+str(w)
            self.resultEdit.setText(unicode(warning,'utf-8','ignore'))
        except MySQLdb.Error,e:
            erro="Cannot delete or update a parent row: "+str(e)
            self.resultEdit.setText(unicode(erro,'utf-8','ignore'))


class Query(QWidget):
    def __init__(self, parent=None):
        super(Query, self).__init__(parent)

        label1 = QLabel(self.tr("表名："))
        label2 = QLabel(self.tr("要查询属性值："))
        label3 = QLabel(self.tr("限制："))
        label4 = QLabel(self.tr("分组："))
        button = QPushButton(self.tr("执行"))
        label5 = QLabel(self.tr("执行结果："))

        self.tableEdit = QLineEdit()
        self.attrEdit = QLineEdit()
        self.limitEdit = QLineEdit()
        self.groupEdit = QLineEdit()
        self.resultEdit = QTextEdit()

        layout = QGridLayout(self)
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.tableEdit, 0, 1)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.attrEdit, 1, 1)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.limitEdit, 2, 1)
        layout.addWidget(label4, 3, 0)
        layout.addWidget(self.groupEdit, 3, 1)
        layout.addWidget(button, 4, 0)
        layout.addWidget(label5, 5, 0)
        layout.addWidget(self.resultEdit, 5, 1)
        self.connect(button, SIGNAL("clicked()"), self.excute)

    def excute(self):
        table = self.tableEdit.text()
        attr = self.attrEdit.text()
        query = "select " + attr + " from " + table
        limit = self.limitEdit.text()
        if len(limit) > 0:
            query += " where " + limit
        #print query
        group = self.groupEdit.text()
        if len(group) > 0:
            query += " group by " + group
        print query
        #        query = "select * from people"
        a2 = cur.execute(str(query))
        info = cur.fetchmany(a2)
        result = ""
        temp=attr.split(',')
        for i in temp:
            result+="   "
            result+=i
        result+='\n\n'
        for i in info:
            for j in i:
                result += " "
                result += str(j)
            result += '\n'
        if len(result) > 0:
            self.resultEdit.setText(result)
        else:
            self.resultEdit.setText("Cannot excute\"" + str(query) + "\"" + ". Or no values return.")


app = QApplication(sys.argv)
main = StockDialog()
main.show()
app.exec_()
conn.commit()
cur.close()
conn.close()