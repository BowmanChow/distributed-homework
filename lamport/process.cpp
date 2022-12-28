#include <stdio.h>
#include <iostream>
#include <unistd.h>
#include "semaphore.h"
#include <string.h>
#include "state.hpp"

constexpr char MESSAGE[] = "me$$age";
constexpr int MESSAGE_SIZE = sizeof(MESSAGE);
constexpr char MARKER[] = "markerr";

constexpr unsigned int READ = 0;
constexpr unsigned int WRITE = 1;

void child_process(int id, int read_fid, int write_fid)
{
    std::cout << "Child " << id << std::endl;

    char in_buffer[MESSAGE_SIZE];
    State self_state;
    bool is_recording = false;

    State record_state;
    char record_channel[MESSAGE_SIZE];

    if (id == 0)
    {
        memcpy(in_buffer, MESSAGE, MESSAGE_SIZE);
        write(write_fid, in_buffer, MESSAGE_SIZE);
    }

    while (read(read_fid, in_buffer, MESSAGE_SIZE))
    {
        if (memcmp(in_buffer, MARKER, MESSAGE_SIZE) == 0)
        {
            std::cout << id << " recieve marker " << std::endl;
            if (is_recording)
            {
            }
            else
            {
                is_recording = true;
                record_state = self_state;
                memset(record_channel, 0, MESSAGE_SIZE);

                write(write_fid, MARKER, MESSAGE_SIZE);
            }
            std::cout << id << " record state : " << record_state.to_string() << std::endl;
            std::cout << id << " record channel : " << record_channel << std::endl;
            is_recording = false;
            continue;
        }
        if (is_recording)
        {
            memcpy(record_channel, in_buffer, MESSAGE_SIZE);
        }

        self_state.push(in_buffer);
        std::cout << id << " recieve : " << self_state.to_string() << std::endl;

        usleep(100000);

        std::string poped = self_state.pop();
        std::cout << id << " send    : " << poped << std::endl;
        write(write_fid, poped.c_str(), poped.size() + 1);

        if (id == 0 && self_state.get_write_times() == 101)
        {
            is_recording = true;
            record_state = self_state;

            std::cout << id << " send    marker " << std::endl;
            write(write_fid, MARKER, MESSAGE_SIZE);
        }
    }
}

int main()
{
    std::cout << MESSAGE << std::endl;
    std::cout << MESSAGE_SIZE << std::endl;

    constexpr int PROCESS_NUM = 2;
    int fid[PROCESS_NUM][PROCESS_NUM][2];

    for (int i = 0; i < PROCESS_NUM; ++i)
        for (int j = 0; j < PROCESS_NUM; ++j)
        {
            if (i != j)
            {
                if (pipe(fid[i][j]) < 0)
                    exit(1);
                std::cout << "open pipe " << fid[i][j][READ] << " " << fid[i][j][WRITE] << std::endl;
            }
        }
    for (int i = 0; i < PROCESS_NUM; ++i)
    {
        for (int j = 0; j < PROCESS_NUM; ++j)
        {
            std::cout << fid[i][j][READ] << "," << fid[i][j][WRITE];
            std::cout << "    ";
        }
        std::cout << std::endl;
    }
    // exit(0);

    if (fork() == 0)
    {
        child_process(0, fid[1][0][READ], fid[0][1][WRITE]);
        return 0;
    }
    if (fork() == 0)
    {
        child_process(1, fid[0][1][READ], fid[1][0][WRITE]);
        return 0;
    }

    std::cout << "parent" << std::endl;

    // write(fid[1][1], MESSAGE, MESSAGE_SIZE);

    int a;
    std::cin >> a;
}