-- comp9311 19s1 Project 1
--
-- MyMyUNSW Solutions


-- Q1:
create or replace view Q1_1(room_id, room_type)
as
select distinct cl.room, r.rtype
from subjects su, courses c, semesters se, classes cl, rooms r
where su.code = 'COMP9311' and se.term = 'S1' and se.year = 2013 and c.subject = su.id and c.semester = se.id and course = c.id and cl.room = r.id 
;

create or replace view Q1(unswid, longname)
as
select unswid, longname
from rooms
where id = (select room_id from Q1_1 where room_type = (select id from room_types where description = 'Laboratory'))
;

-- Q2:
create or replace view Q2(unswid, name)
as
select distinct p.unswid, p.name
from course_enrolments c1, course_staff c2, people p
where c1.student = (select id from people where name = 'Bich Rae') and c1.course = c2.course and c2.staff = p.id
;

-- Q3:
create or replace view Q3_1(id, semester)
as
select ce.student,c.semester 
from subjects s, courses c, course_enrolments ce 
where s.code = 'COMP9311' and s.id = c.subject and c.id = ce.course
;

create or replace view Q3_2(id, semester)
as
select ce.student,c.semester 
from subjects s, courses c, course_enrolments ce 
where s.code = 'COMP9021' and s.id = c.subject and c.id = ce.course
;

create or replace view Q3(unswid, name)
as 
select distinct p.unswid, p.name
from people p, Q3_1 q1, Q3_2 q2, students s
where s.stype = 'intl' and s.id = q1.id and q1.id = q2.id and q1.semester = q2.semester and p.id = q2.id
;

-- Q4:

create or replace view Q4_1(pid, sid)
as
select distinct p.id, pe.student
from programs p, program_enrolments pe
where p.id = pe.program
;

create or replace view Q4_2(pid, num)
as
select pid, count(sid)
from Q4_1
group by pid
;

create or replace view Q4_3(pid, num)
as
select pid, count(sid)
from Q4_1 
where sid in (select id from students where stype = 'intl')
group by pid
;

create or replace view Q4_4(pid, rate)
as
select q2.pid, q3.num * 100 / q2.num
from Q4_2 q2, Q4_3 q3
where q2.pid = q3.pid
;

create or replace view Q4(code, name)
as
select code, name
from programs
where id in (select pid from Q4_4 where rate >= 30 and rate <= 70)
;

--Q5:
create or replace view Q5_1(course, num)
as
select course, count(*)
from course_enrolments
where mark is not null
group by course
;

create or replace view Q5_2(course, minmark)
as 
select q1.course, min(ce.mark)
from Q5_1 q1, course_enrolments ce
where q1.num >= 20 and q1.course = ce.course
group by q1.course
;

create or replace view Q5(code, name, semester)
as
select s. code, s.name, se.name
from Q5_2 q2, courses c, subjects s, semesters se
where q2.course = (select course from Q5_2 where minmark = (select max(minmark) from Q5_2)) and q2.course = c.id and c.subject = s.id and c.semester = se.id
;

-- Q6:
create or replace view Q6_1(num1)
as
select distinct s.id
from stream_enrolments se, students s, program_enrolments pe, streams st
where s.stype = 'local' and pe.student = s.id and pe.semester = (select id from semesters where year = 2010 and term = 'S1') and st.name = 'Chemistry' and se.stream = st.id and pe.id = se.partof
;

create or replace view Q6_2(num2)
as
select distinct s.id
from programs p, program_enrolments pe, students s
where s.stype = 'intl' and pe.student = s.id and pe.semester = (select id from semesters where year = 2010 and term = 'S1') and p.id = pe.program and p.offeredby = (select id from orgunits where name = 'Faculty of Engineering')
;

create or replace view Q6_3(num3)
as
select distinct pe.student
from program_enrolments pe, programs p
where p.id = pe.program and p.code = '3978' and pe.semester = (select id from semesters where year = 2010 and term = 'S1')
;

create or replace view Q6_4(num1)
as
select count(*) from Q6_1 
;

create or replace view Q6_5(num2)
as
select count(*) from Q6_2 
;

create or replace view Q6_6(num3)
as
select count(*) from Q6_3 
;

create or replace view Q6(num1, num2, num3)
as
select q4.num1, q5.num2, q6.num3
from Q6_4 q4, Q6_5 q5, Q6_6 q6
;


-- Q7:
create or replace view Q7_1(id, name, faculty, email, starting)
as
select p.id, p.name, o.longname, p.email, a.starting
from people p, orgunits o, affiliations a
where o.utype = (select id from orgunit_types where name = 'Faculty') and o.id = a.orgunit and a.role = (select id from staff_roles where name = 'Dean') and p.id = a.staff and a.isprimary = 't'
;

create or replace view Q7_2(id, code)
as
select distinct q1.id, s.code
from Q7_1 q1, course_staff cs, courses c, subjects s
where cs.staff = q1.id and c.id = cs.course and s.id = c.subject
;

create or replace view Q7_3(id, num)
as
select q2.id, count(*)
from Q7_2 q2
group by q2.id
;

create or replace view Q7(name, faculty, email, starting, num_subjects)
as
select q1.name, q1.faculty, q1.email, q1.starting, q3.num
from Q7_1 q1, Q7_3 q3
where q1.id = q3.id
;


-- Q8: 
create or replace view Q8_1(id, num)
as
select distinct s.id, count(*)
from courses c, subjects s
where c.subject = s.id
group by s.id
;

create or replace view Q8_2(sid, cid, num)
as
select distinct q1.id, c.id, count(*)
from Q8_1 q1, courses c, course_enrolments ce
where q1.num >= 20 and q1.id = c.subject and c.id = ce.course
group by q1.id,c.id
;

create or replace view Q8_3(sid, num)
as
select sid, count(*)
from Q8_2
where num >= 20
group by sid
;

create or replace view Q8(subject)
as
select s.code ||' ' ||s.name
from Q8_3 q3, subjects s
where q3.sid = s.id and q3.num >= 20
;

-- Q9:
create or replace view Q9_1(sid, year, name)
as
select distinct s.id, se.year, o.longname
from students s, program_enrolments pe, semesters se, orgunits o, programs p
where s.stype = 'intl' and s.id = pe.student and pe.program = p.id and p.offeredby = o.id and se.id = pe.semester
;

create or replace view Q9_2(year, name, num)
as
select year, name ,count(*)
from Q9_1
group by year, name
;

create or replace view Q9_3(num, name)
as
select max(num), name 
from Q9_2
group by name
;

create or replace view Q9(year, num, name)
as
select q2.year, q2.num, q2.name
from Q9_2 q2, Q9_3 q3
where q2.name = q3.name and q2.num = q3.num
;

-- Q10:
create or replace view Q10_1(sid, course, mark)
as
select ce.student, c.id, ce.mark
from semesters se, courses c, course_enrolments ce
where se.year = 2011 and se.term = 'S1' and c.id = ce.course and ce.mark >= 0 and c.semester = se.id
;


create or replace view Q10_2(sid, num)
as
select sid, count(*)
from Q10_1
group by sid
;

create or replace view Q10_3(sid, avg_mark)
as
select q1.sid, (avg(q1.mark))::numeric(4,2) as avg_mark
from Q10_1 q1, Q10_2 q2
where q1.sid = q2.sid and q2.num >= 3
group by q1.sid
order by avg_mark desc
;

create or replace view Q10_4(unswid, name, avg_mark, rankmark)
as
select p.unswid, p.name, avg_mark,rank()over(order by avg_mark desc)
from Q10_3 q3, people p
where p.id = q3.sid
;

create or replace view Q10(unswid, name, avg_mark)
as
select unswid, name, avg_mark
from Q10_4
where rankmark <= 10
;


-- Q11:
create or replace view Q11_1(id, unswid, mark)
as
select distinct p.id, cast(p.unswid as varchar(20)),ce.mark
from people p, semesters se, course_enrolments ce, courses c
where se.year = 2011 and se.term = 'S1' and ce.mark >= 0 and ce.student = p.id and c.semester = se.id and c.id = ce.course
;

create or replace view Q11_2(id,unswid, num)
as
select id, unswid, count(*)
from Q11_1
where unswid like '313%'
group by id, unswid
;

create or replace view Q11_3(id, unswid, num)
as
select id, unswid, count(*)
from Q11_1
where unswid like '313%' and mark >= 50
group by id, unswid
;


create or replace view Q11_4(id, unswid, num)
as
select id, unswid, count(*)
from Q11_1
where unswid like '313%' and mark < 50
group by id, unswid
;

create or replace view Q11_5(id, total_num, rate, standing)
as
select q2.id, q2.num, (q3.num * 100) / q2.num, ac.standing
from Q11_2 q2, Q11_3 q3, academic_standing ac
where q2.id = q3.id
;

create or replace view Q11_6(id, total_num, rate, standing)
as
select q2.id, q2.num, 100 - ((q4.num * 100) / q2.num), ac.standing
from Q11_2 q2, Q11_4 q4, academic_standing ac
where q2.id = q4.id
;

create or replace view Q11_7
as
select * from Q11_5 union select * from Q11_6
;

create or replace view Q11_8(id, rate, standing)
as
select id, rate, standing
from (select * from Q11_5 union select * from Q11_6) as union7_8
where (rate > 50 and standing = 'Good') or (rate <= 50 and rate > 0 and standing = 'Referral') or (rate = 0 and total_num = 1 and standing = 'Referral') or (rate = 0 and total_num > 1 and standing = 'Probation')
;


create or replace view Q11(unswid, name, academic_standing)
as
select p.unswid, p.name, q8.standing
from Q11_8 q8, people p
where q8.id = p.id

;

-- Q12:
create or replace view Q12_1(seid, year, term)
as
select id, year, term
from semesters
where year >= 2003 and year <= 2012 and (term = 'S1' or term = 'S2')
;

create or replace view Q12_2(code, name, id)
as 
select s.code, s.name, s.id 
from subjects s, semesters se, courses c
where se.id in (select seid from Q12_1) and s.code like 'COMP90%' and c.subject = s.id and c.semester = se.id
group by s.code, s.name, s.id
having count(*) >= 20
;

create or replace view Q12_3(subcode, subname, year, s1_tol_num)
as
select q2.code, q2.name, q1.year, count(*)
from Q12_1 q1, Q12_2 q2, courses c, course_enrolments ce
where c.subject = q2.id and c.semester = q1.seid and q1.term = 'S1' and c.id = ce.course and ce.mark >= 0
group by q2.code, q2.name, q1.year
;

create or replace view Q12_4(subcode, subname, year, s1_ps_num)
as
select q2.code, q2.name, q1.year, count(*)
from Q12_1 q1, Q12_2 q2, courses c, course_enrolments ce
where c.subject = q2.id and c.semester = q1.seid and q1.term = 'S1' and c.id = ce.course and ce.mark >= 50
group by q2.code, q2.name, q1.year
;

create or replace view Q12_5(subcode1, subname1, year1, rate1)
as
select q3.subcode, q3.subname, q3.year, (q4.s1_ps_num * 1.0 / q3.s1_tol_num)::numeric(4,2)
from Q12_3 q3, Q12_4 q4
where q3.subcode = q4.subcode and q3.subname = q4.subname and q3.year = q4.year
;

create or replace view Q12_6(subcode, subname, year, s2_tol_num)
as
select q2.code, q2.name, q1.year, count(*)
from Q12_1 q1, Q12_2 q2, courses c, course_enrolments ce
where c.subject = q2.id and c.semester = q1.seid and q1.term = 'S2' and c.id = ce.course and ce.mark >= 0
group by q2.code, q2.name, q1.year
;

create or replace view Q12_7(subcode, subname, year, s2_ps_num)
as
select q2.code, q2.name, q1.year, count(*)
from Q12_1 q1, Q12_2 q2, courses c, course_enrolments ce
where c.subject = q2.id and c.semester = q1.seid and q1.term = 'S2' and c.id = ce.course and ce.mark >= 50
group by q2.code, q2.name, q1.year
;

create or replace view Q12_8(subcode2, subname2, year2, rate2)
as
select q6.subcode, q6.subname, q6.year, (q7.s2_ps_num * 1.0 / q6.s2_tol_num)::numeric(4,2)
from Q12_6 q6, Q12_7 q7
where q6.subcode = q7.subcode and q6.subname = q7.subname and q6.year = q7.year
;

create or replace view Q12_9(subcode, subname, year, s2_ps_num)
as
select q2.code, q2.name, q1.year, count(*)
from Q12_1 q1, Q12_2 q2, courses c, course_enrolments ce
where c.subject = q2.id and c.semester = q1.seid and q1.term = 'S2' and c.id = ce.course and ce.mark < 50
group by q2.code, q2.name, q1.year
;

create or replace view Q12_10(subcode2, subname2, year2, rate2)
as
select q6.subcode, q6.subname, q6.year, (1-(q9.s2_ps_num * 1.0 / q6.s2_tol_num))::numeric(4,2)
from Q12_6 q6, Q12_9 q9
where q6.subcode = q9.subcode and q6.subname = q9.subname and q6.year = q9.year
;

create or replace view Q12_11
as
select * from Q12_8 union select * from Q12_10
;

create or replace view Q12_12
as
select subcode1,subname1, year1, rate1, rate2
from Q12_5 left join Q12_11 on Q12_5.subcode1 = Q12_11.subcode2 and Q12_5.subname1 = Q12_11.subname2 and Q12_5.year1 = Q12_11.year2
;

create or replace view Q12_13
as
select subcode2,subname2, year2, rate1, rate2
from Q12_5 right join Q12_11 on Q12_5.subcode1 = Q12_11.subcode2 and Q12_5.subname1 = Q12_11.subname2 and Q12_5.year1 = Q12_11.year2
;

create or replace view Q12(code, name, year, s1_ps_rate, s2_ps_rate)
as
select subcode1,subname1, substr(cast(year1 as char(4)),3,2), rate1, rate2
from (select * from Q12_12 union select * from Q12_13) as q
order by subcode1,year1
;
