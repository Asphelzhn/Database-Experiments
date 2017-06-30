#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include<QtSql>
#include <QMenu>
#include <qsqldatabase.h>
#include <QSortFilterProxyModel>
#include <QHeaderView>
#include <QSqlTableModel>


namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    ~Widget();

private:
    Ui::Widget *ui;
protected:
    QSqlDatabase db;        //创建数据库类
    bool success;           //是否登陆成功
    int db_port;           //端口号
    QString db_host;            //主机IP
    QString db_name;           //数据库账号
    QString db_password;       //密码

private slots:
    void on_okBtn_clicked();
    void on_canclBtn_clicked();
};

#endif // WIDGET_H
