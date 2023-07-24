#pragma once

#include <QMap>
#include <QDebug>

struct FSMNode
{
    int stateId;

    std::function<void()> entryAction;
    std::function<void()> exitAction;

    QMap<int, std::function<void()>> eventActions;

    QMap<int, int> transitions;
};

class FSMBase : public QObject
{
    Q_OBJECT

public:
    explicit FSMBase(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

    int currentStateId() const
    {
        return _currentStateId;
    }

    void postEvent(int eventId)
    {
        _handleEvent(eventId);
    }

signals:
    void currentStateIdChanged();

protected:
    QString _fsmName;
    QMap<int, FSMNode> _fsmNodes;
    int _currentStateId;

private:
    void _handleEvent(int eventId)
    {
        if (_fsmNodes[_currentStateId].eventActions.contains(eventId))
        {
            _doEventAction(eventId);
        }
        _handleTransition(eventId);
    }

    void _handleTransition(int eventId)
    {
        if (_fsmNodes[_currentStateId].transitions.contains(eventId))
        {
            _doExitAction();
            _goToState(_fsmNodes[_currentStateId].transitions[eventId]);
        }
    }

    void _doEventAction(int eventId)
    {
        _fsmNodes[_currentStateId].eventActions[eventId]();
    }

    void _doEntryAction()
    {
        _fsmNodes[_currentStateId].entryAction();
    }

    void _doExitAction()
    {
        _fsmNodes[_currentStateId].exitAction();
    }

    void _goToState(int stateId)
    {
        qDebug() << _fsmName << "go to state:" << stateId;
        _currentStateId = stateId;
        emit currentStateIdChanged();
        _doEntryAction();
    }
};
