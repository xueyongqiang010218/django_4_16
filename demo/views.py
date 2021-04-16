from django.shortcuts import *
from demo.models import *
import pyecharts.options as opts
from pyecharts.charts import Line
from django.shortcuts import render, HttpResponse
from io import BytesIO
import xlwt
# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    else:
        stuNumber = request.POST.get("stuNumber")
        stuName = request.POST.get("stuName")
        s = Student.objects.filter(stuNumber=stuNumber,stuName=stuName).first()
        # sid = s.id
        # print(s)
        if s:
             sid = request.session['s'] = s
             # stuName = request.session['stuName'] = stuName
             # sid = request.session['user'] = {'sid':sid, 'sname':stuName}

             return redirect("show")
        else:
            return HttpResponse("学号或姓名错误")


def show(request):
    stu_1 = Student.objects.filter(id=request.session['s'].id).first()
    clist = stu_1.chj_set.all()
    wjg = []
    wag = {}
    for i in clist:
        if int(i.cj) < 60:
                wjg.append(i)
    for i in range(1,5):
        www = []
        for w in wjg:
            if w.tid_id == i:
                www.append(w)
        wag['w{}'.format(i)]=www
    # print(wag)
        # if i.kid
        # print(i.kid.kname)


    global tname_list
    tname_list = []
    for tem in Term.objects.all():
        tname_list.append(tem.tname)
    first = []
    second = []
    third = []
    fourth = []
    for c in clist:
        if  c.tid_id == 1:
            first.append(c.cj)
        if c.tid_id == 2:
            second.append(c.cj)
        if c.tid_id == 3:
            third.append(c.cj)
        if c.tid_id == 4:
            fourth.append(c.cj)
    score_list = [first, second, third, fourth]
    # global plist
    # global cclist
    # global c_list
    # global slist
    # plist = []
    # cclist = []
    # c_list = []
    # slist = []
    # for i in clist:
    #     if i.kid_id == 1:
    #         plist.append(i.cj)
    # for i in clist:
    #     if i.kid_id == 2:
    #         cclist.append(i.cj)
    # for i in clist:
    #     if i.kid_id == 3:
    #         c_list.append(i.cj)
    # for i in clist:
    #     if i.kid_id == 4:
    #         slist.append(i.cj)
    global so_dict
    so_dict = {}
    for i in range(1,10):
        chjlist = []
        for s in clist:
            if s.kid_id == i:
                chjlist.append(s.cj)
        so_dict['k{}'.format(i)] = chjlist

    return render(request,'show.html',{
        "clist":score_list,
        'wag': wag,
    })

def line_chart(request):
    x_data = tname_list
    c = (
        Line()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="python",
            y_axis=so_dict['k1'],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="C",
            y_axis=so_dict['k2'],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="C#",
            y_axis=so_dict['k3'],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="C++",
            y_axis=so_dict['k4'],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="JAVA",
            y_axis=so_dict['k5'],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="javascript",
            y_axis=so_dict['k6'],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="PHP",
            y_axis=so_dict['k7'],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="VBS",
            y_axis=so_dict['k8'],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="易语言",
            y_axis=so_dict['k9'],
            label_opts=opts.LabelOpts(is_show=False),
        )

            .set_global_opts(
            title_opts=opts.TitleOpts(title=request.session['s'].stuName),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
        # .render("stacked_line_chart.html")
    )
    return HttpResponse(c.render_embed())

def insert_data(request):
    from random import randint
    stu_list = Student.objects.all()
    for stu in stu_list:
        # if stu.score_set.all():
        #     continue
        subject_list = ['Python', 'C', 'C#', 'C++', 'Java', 'JavaScript', 'PHP', 'VBS', '易语言']
        for subject in subject_list:
            if Kem.objects.filter(kname=subject).first():
                continue
            Kem.objects.create(kname=subject)
        time_list = ['第一学期', '第二学期', '第三学期', '第四学期']
        for time in time_list:
            if Term.objects.filter(tname=time).first():
                continue
            Term.objects.create(tname=time)
        for i in range(1,5):
            for j in range(1,10):
                Chj.objects.create(cj=randint(1,100), sid_id=stu.id, kid_id=j, tid_id=i)
    return HttpResponse('Success')
def download(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='applicationnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=test.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')

    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)

    # 写入文件标题
    sheet.write(0, 0, '序号', style_heading)
    sheet.write(0, 1, '姓名', style_heading)
    sheet.write(0, 2, '学号', style_heading)
    sheet.write(0, 3, '科目', style_heading)
    sheet.write(0, 4, '成绩', style_heading)
    sheet.write(0, 5, '学期', style_heading)

    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    stu_1 = Student.objects.filter(id=request.session['s'].id).first()
    clist = stu_1.chj_set.all()
    for i in clist:
        sheet.write(data_row, 0, i.id)
        sheet.write(data_row, 1, i.sid.stuName)
        sheet.write(data_row, 2, i.sid.stuNumber)
        sheet.write(data_row, 3, i.kid.kname)
        sheet.write(data_row, 4, i.cj)
        sheet.write(data_row, 5, i.tid.tname)
        data_row = data_row + 1

    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response

