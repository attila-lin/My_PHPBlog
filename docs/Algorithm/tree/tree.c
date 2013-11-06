#include <stdio.h>
#include <stdlib.h>

/*
binary search tree:

SearchTree makeempty(SearchTree T)
Position find(int x, SearchTree T)
Position findmin(SearchTree T)
Position findmax(SearchTree T)
SearchTree insert(int x, SearchTree T);
SearchTree delete(int x, SearchTree T);
int retrieve(Position P)

void PrintTree(SearchTree T);
 */

typedef struct treenode * PtrToNode;

struct treenode
{
	/* data */
	int element;
	PtrToNode right;
	PtrToNode left;
};
typedef PtrToNode SearchTree;
typedef PtrToNode Position;

SearchTree makeempty(SearchTree T){
	if( T != NULL){
		makeempty(T->left);
		makeempty(T->right);
		free(T);
	}

	return NULL;
}

Position find(int x, SearchTree T){
	if(T == NULL){
		return NULL;
	}
	else if(x > T->element){
		find(x, T->right);
	}
	else if(x < T->element){
		find(x, T->left);
	}
	else if(T->element == x){
		return T;
	}
}

Position findmax(SearchTree T){
	if(T == NULL){
		return NULL;
	}
	else if(T->right == NULL)
		return T;
	else 
		return findmax(T->right);
}

Position findmin(SearchTree T){
	if(T == NULL){
		return NULL;
	}
	else if(T->left == NULL)
		return T;
	else 
		return findmin(T->left);
}

SearchTree insert(int x, SearchTree T ){
	if( T == NULL ){
		T = (SearchTree)malloc(sizeof( struct treenode ));
		if(T == NULL)
			printf("ERROR\n");
		else{
			T->element = x;
			T->left = T->right = NULL;
		}
	}

	if( x > T->element ){
		T->right = insert(x, T->right);
	}
	else if (x < T->element){
		T->left = insert(x, T->left);
	}

	return T;
}

SearchTree Delete(int x, SearchTree T){
	Position tmpCell;

	if(T == NULL){
		printf("element NOT FOUND\n");
	}
	else if(x < T->element){
		T->left = Delete(x, T->left);
	}
	else if(x > T->element){
		T->right = Delete(x, T->right);
	}
	else if(T->right && T->left){
		tmpCell = findmin(T->right);
		T->element = tmpCell->element;
		T->right = Delete(T->element, T->right);
	}
	else {
		tmpCell = T;
		if(T->left == NULL)
			T = T->right;
		else if(T->right == NULL)
			T = T->left;

		free(tmpCell);
	}

	return T;
}

void PrintTree(SearchTree T){
	if(T == NULL){

	}
	else{
		printf("%d\n", T->element );
		PrintTree(T->left);
		PrintTree(T->right);
	}
}


int main(){
	SearchTree T ;
	T = makeempty(T);
	T =insert(5,T);
	T =insert(2,T);
	T =insert(6,T);
	T =insert(1,T);
	T =insert(9,T);
	T =insert(0,T);
	T =insert(8,T);
	T =insert(3,T);
	PrintTree(T);
	return 0;
}