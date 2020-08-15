#include <iostream>
#include<conio.h>
#include<stdlib.h>

#define MAX_SIZE 15

using namespace std;

void merge_sort(int, int);
void merge_array(int, int, int, int);
clock_t t1,t2;

int arr_sort[MAX_SIZE] = {42, 2, 13, 214, 144, 10, 90, 45, 234, 11, 22, 123, 653, 21};

int main() {
    t1=clock();
    int i;

    
    cout << "Simple C++ Merge Sort Example - Functions and Array\n";
    cout << "\nEnter " << MAX_SIZE << " Elements for Sorting : " << endl;
  

    cout << "\nYour Data   :";
    for (i = 0; i < MAX_SIZE; i++) {
        cout << "\t" << arr_sort[i];
    }

    merge_sort(0, MAX_SIZE - 1);

    cout << "\n\nSorted Data :";
    for (i = 0; i < MAX_SIZE; i++) {
        cout << "\t" << arr_sort[i];
    }

    getch();

}

void merge_sort(int i, int j) {
    int m;

    if (i < j) {
        m = (i + j) / 2;
        merge_sort(i, m);
        merge_sort(m + 1, j);
        // Merging two arrays
        merge_array(i, m, m + 1, j);
    }
    
    t2=clock();
    float diff ((float)t2-(float)t1);
    cout<<"Start:"<<t1<<endl;
    cout<<"Stop:"<<t2;
}

void merge_array(int a, int b, int c, int d) {
    int t[50];
    int i = a, j = c, k = 0;

    while (i <= b && j <= d) {
        if (arr_sort[i] < arr_sort[j])
            t[k++] = arr_sort[i++];
        else
            t[k++] = arr_sort[j++];
    }

    
    
    //collect remaining elements 
    while (i <= b)
        t[k++] = arr_sort[i++];

    while (j <= d)
        t[k++] = arr_sort[j++];

    for (i = a, j = 0; i <= d; i++, j++)
        arr_sort[i] = t[j];
        
        
   
}


      
