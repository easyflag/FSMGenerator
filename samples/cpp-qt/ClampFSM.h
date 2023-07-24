#pragma once

#include <QFile>

#include "ClampFSMDef.h"

class ClampFSM : public ClampFSMDef
{
public:
    ClampFSM(QFile *context)
        : ClampFSMDef(context)
    {
        _context = context;
    }

protected:
    void TightOnEnter() override
    {
        qDebug() << "ClampFSM::TightOnEnter";
        _context->write("TightOnEnter\n");
    }
    void TightOnExit() override
    {
        qDebug() << "ClampFSM::TightOnExit";
        _context->write("TightOnExit\n");
    }
    void TightOnEvent_Trigger() override
    {
        qDebug() << "ClampFSM::TightOnEvent_Trigger";
        _context->write("TightOnEvent_Trigger\n");
    }

    void LooseOnEnter() override
    {
        qDebug() << "ClampFSM::LooseOnEnter";
        _context->write("LooseOnEnter\n");
    }
    void LooseOnExit() override
    {
        qDebug() << "ClampFSM::LooseOnExit";
        _context->write("LooseOnExit\n");
    }
    void LooseOnEvent_Trigger() override
    {
        qDebug() << "ClampFSM::LooseOnEvent_Trigger";
        _context->write("LooseOnEvent_Trigger\n");
    }

private:
    QFile *_context = nullptr;
};
