#ifndef STATE_H
#define STATE_H

#include <string>

class State
{
    int write_times = 0;
    std::string message = "";

public:
    void push(const char *str)
    {
        message = str;
        write_times += 1;
    }

    const std::string pop()
    {
        const std::string res(message);
        message = "";
        return res;
    }

    const std::string pick()
    {
        return message;
    }

    const std::string to_string()
    {
        return message + " " + std::to_string(write_times) + " times";
    }

    const int get_write_times()
    {
        return write_times;
    }
};

#endif
