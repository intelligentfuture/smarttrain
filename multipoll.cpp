#include <stdio.h>   /* Standard input/output definitions */
#include <string.h>  /* String function definitions */
#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */
#include <stdlib.h>
#include <stdint.h>

#include <sqlite3.h>

#include <cstdlib>
#include <pthread.h>

using namespace std;

#define FUNC_CODE       3

uint8_t nodeId = 0;

//char modbuscode[17];

char *nlist;

enum state {IDLE, RECEPTION, END} protState = IDLE;

/*
 * 'open_port()' - Open serial port 1.
 *
 * Returns the file descriptor on success or -1 on error.
 */


int open_port(char* portname, int speed)
{
    struct termios tty;
    int fd = open(portname, O_RDWR | O_NOCTTY | O_SYNC);
    if (fd < 0) {
        printf("Error opening %s: %s\n", portname, strerror(errno));
        return -1;
    }
    
    if (tcgetattr(fd, &tty) < 0) {
        printf("Error from tcgetattr: %s\n", strerror(errno));
        return -1;
    }
    
    cfsetospeed(&tty, (speed_t)speed);
    cfsetispeed(&tty, (speed_t)speed);
    
    tty.c_cflag |= (CLOCAL | CREAD);    /* ignore modem controls */
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;         /* 8-bit characters */
    tty.c_cflag &= ~PARENB;     /* no parity bit */
    tty.c_cflag &= ~CSTOPB;     /* only need 1 stop bit */
    tty.c_cflag &= ~CRTSCTS;    /* no hardware flowcontrol */
    
    /* setup for non-canonical mode */
    tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
    tty.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
    tty.c_oflag &= ~OPOST;
    
    /* fetch bytes as they become available */
    tty.c_cc[VMIN] = 1;
    tty.c_cc[VTIME] = 1;
    
    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        printf("Error from tcsetattr: %s\n", strerror(errno));
        return -1;
    }
    return fd;
}


/*
 
 Modbus Management
 
 */
int process_buffer(char *buf, uint16_t *frame)
{
    int status = 0;
    uint8_t sum = 0;
    uint8_t lrc, i;
    char tmpbuf[] = {0, 0, 0};
    char tmpbuf2[] = {0, 0, 0, 0, 0};
    uint8_t buf_len = strlen(buf);
    if (buf_len >= 8 ) {
        tmpbuf[0] = buf[0];
        tmpbuf[1] = buf[1];
        frame[0] = strtoul(tmpbuf, NULL, 16);
        //  printf("> %d %d %d %d %d %d\n",frame[0],frame[1],frame[2],frame[3],frame[4],frame[5]);
        
        tmpbuf[0] = buf[2];
        tmpbuf[1] = buf[3];
        frame[1] = strtoul(tmpbuf, NULL, 16);
        //  printf(">> %d %d %d %d %d %d\n",frame[0],frame[1],frame[2],frame[3],frame[4],frame[5]);
        
        for (i = 4; i <= buf_len-2; i+=4) {
            tmpbuf2[0] = buf[i];
            tmpbuf2[1] = buf[i+1];
            tmpbuf2[2] = buf[i+2];
            tmpbuf2[3] = buf[i+3];
            frame[i/2] = strtoul(tmpbuf2, NULL, 16);
        }
        //       printf(">>> %d %d %d %d %d %d\n",frame[0],frame[1],frame[2],frame[3],frame[4],frame[5]);
        
        tmpbuf[0] = buf[buf_len-2]; tmpbuf[1] = buf[buf_len-1];
        lrc = strtoul(tmpbuf, NULL, 16);
        for (i = 0; i < 6; i++) {
            sum += frame[i];
        }
        uint8_t mysum = (sum + lrc);
        
        if (mysum == 0) {
            status = 1;
        }
    }
    
    return status;
}

int modbus_parser(char ch, uint16_t *frame)
{
    static char buf[514];
    static int idx = 0;
    static int status = 0;
    
    switch(protState) {
        case IDLE:
            if (ch == ':') {
                protState = RECEPTION;
                idx = 0;
                status = 0;
            }
            break;
        case RECEPTION:
            if ((ch >= '0') && (ch <= '9')) {
                buf[idx++] = ch;
            } else if ((ch >= 'a') && (ch <= 'f')) {
                buf[idx++] = ch;
            } else if ((ch >= 'A') && (ch <= 'F')) {
                buf[idx++] = ch;
            } else if (ch == '\r') {
                buf[idx] = 0;
                protState = END;
            } else {
                protState = IDLE;
            }
            break;
        case END:
            if (ch == '\n') {
                if (process_buffer(buf, frame)) {
                    if ((frame[0] == nodeId) && (frame[1] == FUNC_CODE)) {
                        status = 1;
                        
                    }
                }
            }
            protState = IDLE;
            break;
        default:
            protState = IDLE;
    }
    
    return status;
}

static int callback(void *NotUsed, int argc, char **argv, char **azColName){
    //do nothing
    return 0;
}

int insert(int node,int prev, int occupy){
    printf("%d %d\n",prev,occupy);
    if(prev==0 && occupy==0)
        return 0;
    
    sqlite3 *db;
    
    char *sqlCmd=NULL;
    float p = prev*1.0/1.0;
    float o = occupy*1.0/1.0;
    
    asprintf(&sqlCmd, "INSERT INTO occupy(node,previous,occupy) VALUES(%d,%d*0.1,%d*0.1);",node,prev,occupy);
    
    
    
    char *errMsg = 0;
    int rc;
    rc = sqlite3_open("occupy.db", &db);
    if ( rc ) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return(1);
    }
    rc = sqlite3_exec(db, sqlCmd, callback, 0, &errMsg);
    if ( rc ) {
        fprintf(stderr, "Error: %s\n", errMsg);
        sqlite3_close(db);
        return(1);
    }
    sqlite3_close(db);
    printf("write success\n");    
    return 0;
    
}

//void getmodbus(int nodeId,char *modbuscode){
//    int sum = nodeId+FUNC_CODE+2;
//    sum = 256-sum;
//    sprintf(modbuscode,":%02X%02X%02X%06X%02X\r\n",nodeId,FUNC_CODE,0,2,sum);
//}


int split (char *str, char c, char ***arr)
{
    int count = 1;
    int token_len = 1;
    int i = 0;
    char *p;
    char *t;
    
    p = str;
    while (*p != '\0')
    {
        if (*p == c)
            count++;
        p++;
    }
    
    *arr = (char**) malloc(sizeof(char*) * count);
    if (*arr == NULL)
        exit(1);
    
    p = str;
    while (*p != '\0')
    {
        if (*p == c)
        {
            (*arr)[i] = (char*) malloc( sizeof(char) * token_len );
            if ((*arr)[i] == NULL)
                exit(1);
            
            token_len = 0;
            i++;
        }
        p++;
        token_len++;
    }
    (*arr)[i] = (char*) malloc( sizeof(char) * token_len );
    if ((*arr)[i] == NULL)
        exit(1);
    
    i = 0;
    p = str;
    t = ((*arr)[i]);
    while (*p != '\0')
    {
        if (*p != c && *p != '\0')
        {
            *t = *p;
            t++;
        }
        else
        {
            *t = '\0';
            i++;
            t = ((*arr)[i]);
        }
        p++;
    }
    
    return count;
}

void *PrintHello(void *threadid) {
    
    long *tid;
    tid = (long *)threadid;
    
    
    char **arr = NULL;
    int c =0;
    int i=0;

    c = split(nlist, ',', &arr);
    

    
    

    
    int wr;
    while(1){
        for (i = 0; i < c; i++){
            printf("string #%d: %s\n", i, arr[i]);
            
            
            char modbuscode[17];
            int nodeId = atoi(arr[i];
            int sum = nodeId+FUNC_CODE+2;
            sum = 256-sum;
            sprintf(modbuscode,":%02X%02X%02X%06X%02X\r\n",nodeId),FUNC_CODE,0,2,sum);
            printf("%s %s\n",nodeId,modbuscode);
            wr = write(*tid, modbuscode, 17);
            

        }
        sleep(5);
    }
    
}



int main(int argc,char *argv[]){
    
    int count=0;
    char *pname = argv[1];
    char portname[] = "/dev/ttyACM0";
    sprintf(portname,"/dev/tty%s",pname);
    nlist = argv[2];

    int fd = open_port(portname, B115200);

    pthread_t threads;
    int rc;
    
    rc = pthread_create(&threads, NULL, PrintHello, (void *) &fd);
    
    FILE *fp;
    char str[60];
    
    fp = fopen(portname , "r");
    if(fp == NULL) {
        perror("Error opening file");
        return(-1);
    }
    
    unsigned char vlen;
    int wr;
    while(1){
        
        if( fgets (str, 60, fp)!=NULL ) {
            uint16_t frame[6]={0,0,0,0,0,0};
            
            int i=0;
            
            for(i=0;i<strlen(str);i++)
                modbus_parser(str[i],frame);
            modbus_parser('\n',frame);
            
            printf("%d %d %d %d %d %d\n",frame[0],frame[1],frame[2],frame[3],frame[4],frame[5]);
            if(not (frame[2]==0 && frame[4]==0))
                insert(frame[0],frame[2],frame[4]);
            
        }
        
    }
    close(fd);
    fclose(fp);
    pthread_exit(NULL);

}
