#include "widget.h"
#include "ui_widget.h"
#include"QMessageBox"

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
    ui->line_ip->setText(tr("127.0.0.1"));
    ui->line_paswd->setText(tr("123456"));
    ui->line_port->setText(tr("3306"));
    ui->line_user->setText(tr("root"));
}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_okBtn_clicked()
{
    //链接数据库
    db = QSqlDatabase::addDatabase("QMYSQL");
    //数据库IP
    db_host = ui->line_ip->text();
    db.setHostName(db_host);
    //数据库端口号
    db_port = ui->line_port->text().toInt();
    db.setPort(db_port);
    //数据库密码
    db_password = ui->line_paswd->text();
    db.setPassword(db_password);
    //数据库账号
    db_name = ui->line_user->text();
    db.setUserName(db_name);
    //在mysql数据库中创建mm表，然后链接
    db.setDatabaseName("mm");
    //数据库链接成功返true，失败返回false
    bool success = db.open();
    if(success)
    {
        QMessageBox::information(this,"提示","connect success");
    }
    else
    {
        QMessageBox::information(this,"提示","connect fail");
    }
}

void Widget::on_canclBtn_clicked()
{
    close();
}
