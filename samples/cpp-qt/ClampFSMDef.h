#pragma once

#include "FSMBase.h"

class ClampFSMDef : public FSMBase
{
public:
    enum EventId {
        To_Tight = 1,
        To_Loose = 2,
        Trigger = 3
    };

    enum StateId {
        Tight = 1,
        Loose = 2
    };

    ClampFSMDef(QObject *parent = nullptr)
        : FSMBase(parent)
    {
        _fsmName = "ClampFSM";
        _initTight();
        _initLoose();
        _currentStateId = Loose;
    }

protected:
    virtual void TightOnEnter() = 0;
    virtual void TightOnExit() = 0;
    virtual void TightOnEvent_Trigger() = 0;

    virtual void LooseOnEnter() = 0;
    virtual void LooseOnExit() = 0;
    virtual void LooseOnEvent_Trigger() = 0;

private:
    void _initTight()
    {
        FSMNode node;
        node.stateId = Tight;
        node.entryAction = std::bind(&ClampFSMDef::TightOnEnter, this);
        node.exitAction = std::bind(&ClampFSMDef::TightOnExit, this);
        node.eventActions[Trigger] = std::bind(&ClampFSMDef::TightOnEvent_Trigger, this);
        node.transitions[To_Loose] = Loose;
        _fsmNodes[Tight] = node;
    }

    void _initLoose()
    {
        FSMNode node;
        node.stateId = Loose;
        node.entryAction = std::bind(&ClampFSMDef::LooseOnEnter, this);
        node.exitAction = std::bind(&ClampFSMDef::LooseOnExit, this);
        node.eventActions[Trigger] = std::bind(&ClampFSMDef::LooseOnEvent_Trigger, this);
        node.transitions[To_Tight] = Tight;
        _fsmNodes[Loose] = node;
    }
};
