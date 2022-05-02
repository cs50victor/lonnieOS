/*
 VICTOR ATASIE
 # https://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf
 ferry can only hold 4 people,
        only leaves if 4 people are in it
        possible combination:
                    2 hackers + 2 serfs,
                    4 hackers
                    4 serfs
       every entry on the boat invokes the board
  one thread calls the rowBoat function
  algorithm only needs to factor one way travel
*/
#include <pthread.h>
#include <semaphore.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_OF_THREADS 5

pthread_barrier_t ferryBarrier;
sem_t mutex, hackerQueue, serfQueue;
int hackers = 0, serfs = 0;

void *ferry(void *);
void board(long);
void rowBoat(int, int);

int main(int argc, char *argv[]) {

  sem_init(&mutex, 0, 1);
  sem_init(&hackerQueue, 0, 0);
  sem_init(&serfQueue, 0, 0);
  pthread_barrier_init(&ferryBarrier, NULL, 4);

  pthread_t th[NUM_OF_THREADS];

  for (int i = 0; i < NUM_OF_THREADS; i++) {
    if (pthread_create(th + i, NULL, ferry, (void *)i)) {
      printf("ERROR creating thread %d. \n", i);
      exit(1);
    }
    // printf("Thread %d was created.\n", i);
  }
  for (int i = 0; i < NUM_OF_THREADS; i++) {
    if (pthread_join(th[i], NULL)) {
      printf("ERROR joining thread %d. \n", i);
      exit(1);
    }
    // printf("Thread %d finished execution.\n", i);
  }

  sem_destroy(&mutex);
  sem_destroy(&hackerQueue);
  sem_destroy(&serfQueue);
  pthread_barrier_destroy(&ferryBarrier);

  pthread_exit(NULL);
  return 0;
}

void *ferry(void *id) {
  srand(time(NULL));
  sem_wait(&mutex);
  long tid = (long)id;

  // using these because global vairbales are changed to 0 before rowBoat
  // function is called by a thread.
  int hackersTemp = 0, serfsTemp = 0;
  bool isCaptain = false;
  if (rand() % 2 + 1 == 1) {
    hackers += 1;
    printf("\nThread [%ld] is a hacker.\n", tid);
  } else {
    serfs += 1;
    printf("\nThread [%ld] is a serf.\n", tid);
  }

  if (hackers == 4 || serfs == 4) {
    hackersTemp = hackers;
    serfsTemp = serfs;
    if (hackers == 4) {
      hackers = 0;
    } else {
      serfs = 0;
    }
    isCaptain = true;
  } else if ((hackers == 2 && serfs >= 2) || (hackers >= 2 && serfs == 2)) {
    if (hackers >= 2 && serfs == 2) {
      serfsTemp = serfs;
      hackers -= 2;
      hackersTemp = 2;
      serfs = 0;
    } else {
      hackersTemp = hackers;
      serfs -= 2;
      serfsTemp = 2;
      hackers = 0;
    }
    isCaptain = true;
  } else {
    sem_post(&mutex);
  }

  board(tid);
  puts("\nFerry barrier is waiting for more passengers ......\n");
  pthread_barrier_wait(&ferryBarrier);

  if (isCaptain) {
    rowBoat(hackersTemp, serfsTemp);
    sem_post(&mutex);
  } else {
    
  }
}

void board(long id) { printf("\nThread [%ld] has boarded the ferry.\n", id); }

void rowBoat(int hackers, int serfs) {
    printf("\n\n..... FERRY CROSSIING RIVER 🛳 ........\nLinux hackers - %d  | Microsoft employees (serfs) %d ]\n\n",hackers, serfs);
}
