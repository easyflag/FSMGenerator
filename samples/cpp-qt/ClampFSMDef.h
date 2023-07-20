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

    ClampFSMDef()
        : FSMBase()
    {
        _fsmName = "ClampFSM";
        _initTight();
        _initLoose();
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
        node.id = Tight;
        node.entryAction = [this]() {
            TightOnEnter();
        };
        node.exitAction = [this]() {
            TightOnExit();
        };
        node.eventActions[Trigger] = [this]() {
            TightOnEvent_Trigger();
        };
        node.transitions[To_Loose] = Loose;
        _fsmNodeTab[Tight] = node;
    }

    void _initLoose()
    {
        FSMNode node;
        node.id = Loose;
        node.entryAction = [this]() {
            LooseOnEnter();
        };
        node.exitAction = [this]() {
            LooseOnExit();
        };
        node.eventActions[Trigger] = [this]() {
            LooseOnEvent_Trigger();
        };
        node.transitions[To_Tight] = Tight;
        _fsmNodeTab[Loose] = node;
    }
};
