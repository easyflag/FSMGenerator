#pragma once

#include <QFile>

#include "ClampFSMDef.h"

class ClampFSM : public ClampFSMDef
{
public:
    ClampFSM(QFile *context)
        : ClampFSMDef()
    {
        _context = context;
//        _init();
    }

protected:
    void TightOnEnter() override   {
        qDebug() << "ClampFSM::TightOnEnter";
        qDebug() << _context->write("TightOnEnter\n");
    }
    void TightOnExit() override   {
        qDebug() << "ClampFSM::TightOnExit";
        qDebug() << _context->write("TightOnExit\n");
    }
    void TightOnEvent_Trigger() override   {
        qDebug() << "ClampFSM::TightOnEvent_Trigger";
    }

    void LooseOnEnter() override   {
        qDebug() << "ClampFSM::LooseOnEnter";
        qDebug() << _context->write("LooseOnEnter\n");
    }
    void LooseOnExit() override   {
        qDebug() << "ClampFSM::LooseOnExit";
        qDebug() << _context->write("LooseOnExit\n");
    }
    void LooseOnEvent_Trigger() override   {
        qDebug() << "ClampFSM::LooseOnEvent_Trigger";
    }

private:
    QFile *_context = nullptr;
};
