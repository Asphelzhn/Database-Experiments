#!/usr/bin/python
# -*- coding: gbk -*-
# -*- coding: utf-8 -*-
#encoding=UTF-8
import MySQLdb

conn=MySQLdb.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="",
    db="lee",
    charset='utf8'
    )
cur=conn.cursor()

flag=input("������������(1--9): ")
if flag==1:
    pno=raw_input("��������Ŀ���:") #�μ�����Ŀ���Ϊ%PNO%����Ŀ��Ա����
    tmp = 'select distinct essn from employee natural join project where pno = "'+pno+'"'
    a1=cur.execute(tmp)
    info = cur.fetchmany(a1)
    print "�μ�����Ŀ���Ϊ" + pno +"��Ա�����Ϊ��"
    for i in info:
        for j in i:
            print j
            
elif flag==2:
    pname=raw_input("��������Ŀ����:")#�μ�����Ŀ��Ϊ%PNAME%��Ա������
    tmp = 'select distinct ename from employee natural join project where pname = "'+pname+'"'
    a2=cur.execute(tmp.decode("gbk").encode("utf8"))
    info = cur.fetchmany(a2)
    print "�μ�����Ŀ��" + pname +"��Ա�������У�"
    for i in info:
        for j in i:
            print j

elif flag==3:        
    dname=raw_input("�����벿������:")#��%DNAME%���������й�����Ա�����ֺ͵�ַ
    tmp = 'select distinct ename, address from department natural join employee where dname = "'+dname+'"'
    a3=cur.execute(tmp.decode("gbk").encode("utf8"))
    info = cur.fetchmany(a3)
    print "��" + dname +"���Ź�����Ա�����͵�ַ���£���������ַ������֣���"
    for i in info:
        for j in i:
            print j

elif flag==4:
    dname=raw_input("�����벿������:")#��%DNAME%�����ҹ��ʵ���%SALARY%Ԫ��Ա�����ֺ͵�ַ
    salary=input("�����빤��Ǯ��:")
    tmp = 'select distinct ename, address, dname, salary from department natural join employee where dname = "'+dname+'" '+' and salary < '+str(1300);
    a4=cur.execute(tmp.decode("gbk").encode("utf8"))
    info = cur.fetchmany(a4)
    print "��" + dname +"���Ź����ҹ��ʵ���" + str(salary) +"��Ա�����͵�ַ���£���������ַ������֣���"
    for i in info:
        for j in i:
            print j

elif flag==5:
    pno=raw_input("��������Ŀ���:")#û�вμ���Ŀ���Ϊ%PNO%����Ŀ��Ա������
    a5=cur.execute("select distinct ename from employee where essn not in (select essn from works_on where pno=%s)",pno)
    info = cur.fetchmany(a5)
    print "û�вμ���Ŀ���Ϊ��" + pno + "��Ա���������£�"
    for i in info:
        for j in i:
            print j

elif flag==6:
    ename=raw_input("�������쵼����:")#��%ENAME%�쵼�Ĺ�����Ա�����������ڲ��ŵ�����
    a6=cur.execute("select ename,dname from employee,department where employee.dno=department.dno\
                and superssn=(select essn from employee where ename=%s)",ename)
    info = cur.fetchmany(a6)
    print "��" + ename + "�쵼�Ĺ�����Ա���������ڲ����������£��������������ֽ�����֣���"
    for i in info:
       for j in i:
            print j

elif flag==7:
    pno1=raw_input("�������һ����Ŀ���:")#���ٲμ�����Ŀ���Ϊ%PNO1%��%PNO2%����Ŀ��Ա����
    pno2=raw_input("������ڶ�����Ŀ���:")
    strall="select essn from employee where essn in (select essn from works_on where " + "pno="+"'"+ pno1 +"'"\
          + " and essn in (select essn from works_on where pno=" + "'" +pno2 + "'))"
    a7=cur.execute(strall)
    info = cur.fetchmany(a7)
    print "���ٲμ�����Ŀ���Ϊ" + pno1 + "��" + pno2 + "��Ա�����Ϊ��"
    for i in info:
        for j in i:
            print j
            
elif flag==8:        
    salary=input("�����빤��Ǯ��:")#Ա��ƽ�����ʵ���%SALARY%Ԫ�Ĳ�������
    a8=cur.execute("select dname from employee,department where employee.dno=department.dno\
                    group by employee.dno having avg(salary)<%s",salary)
    info = cur.fetchmany(a8)
    print "Ա��ƽ�����ʵ���" + str(salary) + "�Ĳ��������У�"
    for i in info:
        for j in i:
            print j

elif flag==9:
    num=input("������μ���Ŀ��:")#���ٲ�����%N%����Ŀ�ҹ�����ʱ�䲻����%HOURS%Сʱ��Ա������
    hours=input("������ʱ��:")
    strall="select employee.ename from employee where essn in (select essn from works_on \
            group by essn having count(*)>" + str(num) +" and sum(hours)<=" + str(hours) + ")"
    a9=cur.execute(strall)
    info = cur.fetchmany(a9)
    print "�μ��˶���" + str(num) + "����Ŀ�ҹ�����ʱ�����" + str(hours) + "��Ա���������£�"
    for i in info:
        for j in i:
            print j

else:
    print "û����������������ţ�"
conn.commit()
cur.close()
conn.close()
