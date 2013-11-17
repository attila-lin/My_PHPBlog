#include <stdio.h>
#include <malloc.h>

#ifndef _List_H

struct  Node;
typedef struct Node * PtrToNode;
typedef PtrToNode List;
typedef PtrToNode Position;


List InitAList();
List MakeEmpty(List L);
int IsEmpty(List L);
int IsLast(List L, Position P);
Position Find(List L, int X);
void Delete(List L, int X);
Position FindPrevious(List L,int X);
void Add(int X, List L);
void Insert(int X, List L, Position P);
void DeleteList(List L);
Position First(List L);
Position Last(List L);
Position Advance(Position P);
int Retrieve(Position P);
Position Last(List L);
void PrintList(List L);

#endif /* _List_H */

struct Node
{
    int element;
    PtrToNode Next;
};

List InitAList(){
    List L = (List) malloc(sizeof(List));
    L->Next = NULL;
    return L;
}

List MakeEmpty(List L){
    Position p = L->Next;
    while(p != NULL){
        Position tmep = p->Next;
        free(p);
        p = tmep;
    }
    L->Next = NULL;
    return L;
}

int IsEmpty(List L){
    // if( L->Next == NULL){
    //  return 1;
    // }
    // else{
    //  return 0;
    // }

    // EASIER WAY
    return L->Next == NULL;
}

int IsLast(List L, Position P){
    return P->Next == NULL;
}

Position Find(List L, int X){
    Position s = L->Next;
    while(s->Next != NULL && s->element != X){
        s = s->Next;
    }
    return s;
}

void Delete(List L, int X){
    Position prep = L;
    while(prep->Next->Next != NULL && prep->Next->element != X){
        prep = prep->Next;
    }
    Position thisp = prep->Next;
    Position laterp = thisp->Next;
    prep->Next = laterp;
    free(thisp);
}

void Add(int X, List L){
    Position lastp = Last(L);
    Position thisp = (Position)malloc(sizeof(Position));
    thisp->element = X;
    thisp->Next = NULL;

    lastp->Next = thisp;
}

Position Last(List L){
    while(L->Next != NULL){
        L = L->Next;
    }
    return L;
}

void PrintList(List L){
    L = L->Next;
    while(L->Next == NULL){
        printf("%d\n", L->element);
        L = L->Next;
    }
}

int main(int argc, char const *argv[])
{
    List L = InitAList();
    L = MakeEmpty(L);

    Add(1, L);
    Add(2, L);

    PrintList(L);

    return 0;
}