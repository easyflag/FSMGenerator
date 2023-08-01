/* This file is auto generated,don't modfiy it. */

#pragma once

#include "FSMBase.h"

class ClampFSMDef : public FSMBase
{
public:
    enum EventId {
        TO_TIGHT = 1,        
        TO_LOOSE = 2,        
        TRIGGER = 3        
    };

    enum StateId {
        TIGHT = 1,        
        LOOSE = 2        
    };

    ClampFSMDef(QObject *parent = nullptr)
        : FSMBase(parent)
    {
        _fsmName = "ClampFSM";

        _initTIGHT();
        _initLOOSE();
     
        _currentStateId = LOOSE;
    }

protected:
    /// need implement: do something
    virtual void TIGHTOnEnter() = 0;

    /// need implement: do something
    virtual void TIGHTOnExit() = 0;

    /// need implement: do something
    virtual void TIGHTOnEvent_TRIGGER() = 0;
    
    /// need implement: do something
    virtual void LOOSEOnEnter() = 0;

    /// need implement: do something
    virtual void LOOSEOnExit() = 0;

    /// need implement: do something
    virtual void LOOSEOnEvent_TRIGGER() = 0;

private:
    void _initTIGHT()
    {
        FSMNode node;
        node.stateId = TIGHT;
        node.entryAction = std::bind(&ClampFSMDef::TIGHTOnEnter, this);
        node.exitAction = std::bind(&ClampFSMDef::TIGHTOnExit, this);
        node.eventActions[TRIGGER] = std::bind(&ClampFSMDef::TIGHTOnEvent_TRIGGER, this);
        node.transitions[TO_LOOSE] = LOOSE;
        _fsmNodes[TIGHT] = node;
    }

    void _initLOOSE()
    {
        FSMNode node;
        node.stateId = LOOSE;
        node.entryAction = std::bind(&ClampFSMDef::LOOSEOnEnter, this);
        node.exitAction = std::bind(&ClampFSMDef::LOOSEOnExit, this);
        node.eventActions[TRIGGER] = std::bind(&ClampFSMDef::LOOSEOnEvent_TRIGGER, this);
        node.transitions[TO_TIGHT] = TIGHT;
        _fsmNodes[LOOSE] = node;
    }
};
