###########Code an automatic theorem prover for propositional logic using resolution###################
#sample input-output
#Input: (from stdin)
#6
#p,~q=>p
#p|q,~q|r=>p|r
#p|q,~q|r=>r
#p|q,p->r,q->r=>r
#(p->q)->q,(p->p)->r,(r->s)->(~s->q)=>r
#(p->q)->q,(p->p)->r,(r->s)->(~s->q)=>p

#Output: (to stdout)
#	1
#	1
#	0
#	1
#	1
#	0
#p^~p has p and ~p as clauses, thus reduces to null, thus ans // not very sure about it. though, p|~p iks a tautology thus has to be true. 
# p^~p should be zero

#!usr/bin/env python

import shlex

prio = {'~':7, '^':6,'|':5,'%':4,'$':3,'(':2,')':1}        ##      % is ->     $ is <->

def topostfix(infix_src):
    postfix = list()
    stack = list()
    for x in shlex.shlex(infix_src):
    	if x.isalpha():
            postfix.append(x)
        if x in '$%|^~':
            while len( stack ) and prio[x] < prio[ stack[-1]]:
                postfix.append( stack.pop() )
            stack.append(x)
        if x == '(':
            stack.append(x)
        if x == ')':
            while stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()

    while len(stack):
        if(stack[-1] == "("):
            stack.pop()
        else:
            postfix.append( stack.pop() )

    return postfix
def cnf_1(list_tree):
	if len(list_tree) >1:
		if(list_tree[-2]=='%'):
			list_tree[-2] = '|'
			pqr = cnf_1(list_tree[2])
			list_tree[2] = pqr
#			print list_tree[2],"list_tree2"
#			list_tree[1] = cnf_1(list_tree[1])
			if len(list_tree[0])!=1:
				b = list()
				b.append('~')
				list_tree[0] = [list_tree[0]]
				list_tree[0].append(b)
				list_tree[0].reverse()
			elif len(list_tree[0])==1 :
				a = list_tree[0]
				list_tree[0] = list()
				list_tree[0].append('~')
				list_tree[0].append(a)
			abc = cnf_1(list_tree[0])
#			print abc 
			list_tree[0] = abc
		else:
			for i in range(len(list_tree)):
				list_tree[i] = cnf_1(list_tree[i])
		return list_tree
	return list_tree

def cnf_2(list_tree):
	if(len(list_tree) > 1):
		if(list_tree[-2]=='$'):
			list_tree[-2] = '%'
			list_tree = [list_tree]
			abc = list_tree[0][:]
			list_tree.append('^')
			abc.reverse()
#			print abc, "this is abc"
			list_tree.append(abc)
#			print list_tree,"this is list_tree"
		if len(list_tree)==3:
			list_tree[0]= cnf_2(list_tree[0])
			list_tree[2]= cnf_2(list_tree[2])
		return list_tree
	return list_tree

def change(tree):
       new=[]
       if len(tree[1][0]) == 2:                                    ## not'ed alphabet
               new.append(tree[1][0][1])
#	       print "hey"
       else:
               app=['~', tree[1][0]]
               new.append(app)

       if tree[1][1]=='^':
               new.append('|')
       else:
               new.append('^')

       if len(tree[1][2]) == 2:
               new.append(tree[1][2][1])
#              print "hey"
       else:
               app=['~', tree[1][2]]
               new.append(app)
       return new

       
       
def demorgan(tree):
       if len(tree)==1:
#	       print "length of tree ",len(tree)
	       if len(tree[0])!=1 :
               		ans=demorgan(tree[0])
               		ans=ans
	       else :
	      		ans = [tree]
       elif len(tree) == 2:
               if len(tree[1]) == 3:
                       new=change(tree)
                       ans=demorgan(new)
		
	       elif len(tree[1]) ==2 : 
		       ans = [tree[1][1]]
	
	       else:	
                       return tree

       else:
               res=[]
               if len(tree[0]) == 2:
                       if len(tree[0][1]) == 3:
                               new=change(tree[0])
                               res.append(new)
                       else:
                               res.append(tree[0])
               else:
                       res.append(tree[0])

               res.append(tree[1])

               if len(tree[2]) == 2:
                       if len(tree[2][1]) == 3:
                               new=change(tree[2])
                               res.append(new)
                       else:
                               res.append(tree[2])
               else:
                       res.append(tree[2])

               if len(res[0]) == 3:
                       res1=demorgan(res[0])
               else:
                       res1=res[0]
               if len(res[2]) == 3:
                       res2=demorgan(res[2])
               else:
                       res2=res[2]
               ans=[res1, res[1], res2]
       return ans
		  	

def distribution(list_tree):
#	print list_tree, " this is the tree "
	if len(list_tree)== 3 :	
		if list_tree[1] == '|' :
			if(len(list_tree[0]) == 3):
				if list_tree[0][1] == '^' :
					list_tree[1] = '^'
					ans = []
					ans = [list_tree[0][0],'|',list_tree[2]]
					ans1 = []
					ans1 = [list_tree[0][2],'|',list_tree[2]]
					list_tree.pop(0)
					list_tree.insert(0,ans)
					list_tree.pop()
					list_tree.append(ans1)
				list_tree[0] = distribution(list_tree[0])
			if(len(list_tree[2])==3):
				if list_tree[2][1] == '^' :
					list_tree[1] = '^'
					ans2 = []
					ans2 = [list_tree[2][0],'|',list_tree[0]]
					ans3 = []
					ans3 = [list_tree[2][2],'|',list_tree[0]]
					list_tree.pop(0)
					list_tree.insert(0,ans2)
					list_tree.pop()
					list_tree.append(ans3)
				list_tree[2] = distribution(list_tree[2])
		else :
			list_tree[0] = distribution(list_tree[0])
			list_tree[2] = distribution(list_tree[2])
#	if len(list_tree)==1 :
#	   	return list_tree
#	for i in range(len(list_tree)):
#		list_tree[i] = distribution(list_tree[i])
	return list_tree
				
				
				
		



def conv_tree(string):
	list1 = list()

	for x in string:
		if x.isalpha():
			list1.append(x)
		if x in '$%|^':
			list2 = list()
		 	a = list1.pop()
		 	b = list1.pop()
		 	list2.append(b)
		 	list2.append(x)
		 	list2.append(a)
#			print list2
		 	list1.append(list2)
#			print list1
		if x in '~':
			list2 = list()
		 	c = list1.pop()
		 	list2.append('~')
		 	list2.append(c)
		 	list1.append(list2)
#		 	print list1

	return list1[0]

global list_clause
list_clause = list()
def create_clauses(list_tree):
	global list_clause
	if(len(list_tree)==3):
		if list_tree[1] =='^' :
			if(len(list_tree[0])==3):
#				if(list_tree[0][1] == '|'):
#					list_clause.append(list_tree[0])
#				else :
			 		create_clauses(list_tree[0])
			elif(len(list_tree[0])<=2):
				list_clause.append(list_tree[0])
			else:
#				print "other part being called"
				create_clause(list_tree[0])

			if(len(list_tree[2])==3):
#				if(list_tree[2][1]=='|'):
#					list_clause.append(list_tree[2])
#				else: 
					create_clauses(list_tree[2])
			elif(len(list_tree[2])<=2):
				list_clause.append(list_tree[2])
			else : 
				create_clause(list_tree[2])
		else :
			list_clause.append(list_tree)
	else : 
		list_clause.append(list_tree)	

def resolution():
	n=1
	arr = []
	temp = []
	for i in range(len(list_clause)):
		if(len(list_clause) == 3):
			if(list_clause[1]=='|'):
				list_clause.remove('|')
		if(len(list_clause[i])==3):
			if(list_clause[i][1] == '|'):
				list_clause[i].remove('|')
		if(len(list_clause[i])==2 and list_clause[i].count('~')>0):
			list_clause[i] = [list_clause[i]]
#	print "this is the list of clauses",list_clause
	for i in list_clause:
	  if(len(i)==2):
		  if(len(i[1])==2):
			  if(i[0]==i[1][-1]):
				  list_clause.remove(i)
		  elif(len(i[0])==2):
			  if(i[1]==i[0][-1]):
				  list_clause.remove(i)
	while n!=0:
		n=0								#write code to check if two literals are same in one clause, remove that clause	
		for clause1 in list_clause:
	       		for literal1 in clause1:
	  			n=0
				for clause2 in list_clause :
					temp = []
					for literal2 in clause2 :
					 	add = 0
						if len(literal1)==2 :
							if(literal1[-1] == literal2):
#								print literal1,"of clause ",clause1 ,"has a complement as ",literal2,"of clause",clause2
								for i in range(len(clause1)):
									if(clause1[i]!=literal1):
										temp.append(clause1[i])
								for i in range(len(clause2)):
									if(clause2[i]!=literal2):
										temp.append(clause2[i])
#								print "newly added clause ", temp


								if temp ==[] :
								  	print 1
								  	return
								for i in temp:
									for j in temp:
										if(len(i)==2):
											if(i[-1]==j):
												add = 1;
								if add==0:
									list_clause.append(temp)
								n=1


	if list_clause==[]:
		print 1
		return
	print 0
	return	

								
 		

def main():
	global list_clause
	n = int(raw_input())
	for p in range(n):
		a = raw_input()
		x =[]
		a = a.replace('->','%')
		a = a.replace('<->','$')
		two_input = a.split("=>")
		if len(two_input)==2 :
			conclusion = two_input[1]
		if two_input[0]!= '' :
			inputx = two_input[0]
			x = inputx.split(",")
		if len(two_input)==2 :
			conclusion = "(~("+conclusion+"))"
		x.append(conclusion)
		for i in x :
			y= topostfix(i)
			tree = conv_tree(y)
			tree = cnf_2(tree)
			tree = cnf_1(tree)
			tree = demorgan(tree)
			tree = distribution(tree)
			create_clauses(tree)

		resolution()
		list_clause = []
		

if __name__ == "__main__":
	main()
