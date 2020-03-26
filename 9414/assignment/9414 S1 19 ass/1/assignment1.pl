%Full name: Tian Liu
%Student number: z5230310
%Assignment name: Prolog programming
%Date: 14/3/2019
%

%test 1
%Purpose: Write a predicate sumsq_even(Numbers,Sum) that sums the squares 
%         of only the only the even numbers in a list of integers.
%

%base case
%
sumsq_even([], 0).

%recursive case
%

sumsq_even([H|T], Sum) :-
	0 is H mod 2,
	sumsq_even(T,S),
	Sum is H * H + S.

sumsq_even([H|T], Sum) :-
	not(0 is H mod 2),
	sumsq_even(T,Sum).

%test 2
%Purpose: Write a predicate same_name(Person1,Person2) that succeeds if it
%		  can be deduced from the facts in the database that Person1 and 
%		  Person2 will have the same family name.
%


parent(s,r).
parent(r,t).


% ancesor(Person1, Person2) :- Person1 is ancesor of Person2
%
ancesor(Person1,Person2) :-
	parent(Person1,Person2);
	parent(Person2,Person1).

ancesor(Person1,Person2) :-
	parent(Person1,X),
	parent(X,Person2);
	parent(Person2,X),
	parent(X,Person1).

%same_name(Person1,Person2) :- Person1 and Person2 have the same family name
%
same_name(Person1,Person2) :-
	ancesor(Person1,Person2),
	male(Person1).

same_name(Person1,Person2) :-
	ancesor(Person2,Person1),
	male(Person2).


%test3
%Purpose:Write a predicate sqrt_list(NumberList, ResultList) that binds 
%		 ResultList to the list of pairs consisting of a number and its 
%		 square root, for each number in NumberList. 
%


%base case
%
sqrt_list([],[]).

%recursive case
%
sqrt_list([H|T], Result) :-
	H >= 0,
	Sqrt is sqrt(H),
	sqrt_list(T,R),
	Result = [[H,Sqrt]|R].

sqrt_list([H|T], Result) :-
	H < 0,
	sqrt_list(T,Result).	



%test4
%Purpose:Write a predicate sign_runs(List, RunList) that converts a list of 
%		 numbers into the corresponding list of sign runs.
%

%same_number(X,Y) :- X and Y are both positive or negative numbers
%
same_number(X,Y) :-
	X >= 0,
	Y >= 0.
same_number(X,Y) :-
	X < 0,
	Y < 0.

%different_number(X,Y) :- X and Y have different sign
%
different_number(X,Y) :-
	X >= 0,
	Y < 0.
different_number(X,Y) :-
	X < 0,
	Y >= 0.

%base case
%
sign_runs([],[]).
sign_runs([Number],[[Number]]).

%recursive case
%
sign_runs([Before|[After|Rest_L]], [[Before|Same_L]|New_Rest_L]) :-
	same_number(Before,After),
	sign_runs([After|Rest_L],[Same_L|New_Rest_L]).

sign_runs([Before|[After|Rest_L]], [[Before]|New_Rest_L]) :-
	different_number(Before,After),
	sign_runs([After|Rest_L],New_Rest_L).


%test5
%Purpose:Write a predicate is_heap(Tree) which returns true if Tree satisfies 
%	     the heap property, and false otherwise.
%

%base case
%
is_heap(tree(empty,_,empty)).

%recursive case
%
is_heap(tree(empty, Value, tree(Left,Part_Value,Right))) :- 
	Value =< Part_Value,
	is_heap(tree(Left, Part_Value, Right)).
is_heap(tree(tree(Left,Part_Value,Right), Value, empty)) :- 
	Value =< Part_Value,
	is_heap(tree(Left,Part_Value,Right)).
is_heap(tree(tree(Left1,Part_Value1,Right1), Value, tree(Left2,Part_Value2,Right2))) :- 
	Value =< Part_Value1,
	Value =< Part_Value2,
	is_heap(tree(Left1,Part_Value1,Right1)),
	is_heap(tree(Left2,Part_Value2,Right2)).

	
	








